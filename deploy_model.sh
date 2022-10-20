experiment_name=$1
EXPERIMENT_REGEX="^(random)"


if [[ $experiment_name =~ $EXPERIMENT_REGEX ]]; then
    set -o pipefail -e
    params=$(kubectl get experiment $experiment_name -n kubeflow-user-example-com -o jsonpath={.status.currentOptimalTrial.parameterAssignments}  | jq '.')
    set +o pipefail +e
    git checkout dev
    git pull origin dev
    rm .dvc/cache -rf
    declare -A params_dict
    x=0
    while [ $x -le 7 ];
    do
        key=$(echo $params | jq ".[$x]" | jq .name | cut -d '"' -f 2)
        value=$(echo $params | jq ".[$x]" | jq .value | cut -d '"' -f 2)
        params_dict[$key]=$value
        ((x+=1))
    done
    python main.py \
    --eta=${params_dict[eta]} \
    --gamma=${params_dict[gamma]} \
    --max-depth=${params_dict[max-depth]} \
    --min-child-weight=${params_dict[min-child-weight]} \
    --subsample=${params_dict[subsample]} \
    --colsample-bytree=${params_dict[colsample-bytree]} \
    --reg-alpha=${params_dict[reg-alpha]} \
    --reg-lambda=${params_dict[reg-lambda]}

    old_run_id=$(cat seldon_deployment/mlflow-model-serving.yaml | grep s3 | cut -d "/" -f 8)
    new_run_id=$(cat run_id.txt)

    sed -i "s/$old_run_id/$new_run_id/" seldon_deployment/mlflow-model-serving.yaml

    git add seldon_deployment/ensemble-model.yaml && git commit -m "chage model path" && git push origin dev
else
    echo "execute with right experiment name !!!"
    exit
fi

# MLflow
- 모두의 MLOps 기준으로 model registry로 mlflow를 사용한다. 그리고 backend로 postgresql을 사용하고 remote strage로 kubeflow시 설치되는 minio를 사용한다.
## 발생한 문제와 해결
### ver.1
- remote storage를 amazon s3로 바꾸는 과정에서 mlflow server의 `default-artifact-root` 를 s3로 수정하고 env에 s3 credential을 넣어도 s3 object 위치를 제대로 읽지 못하는 경우가 발생했음
- 내부 코드를 살펴보면서 object 위치를 어떻게 지정하는지 봤는데 지정한대로 경로를 파싱하지 않고 있었기에 mlflow 내부 코드를 수정하여 s3 디렉토리를 제대로 가리키도록 함
- 하지만 s3 credential이 dockerfile을 빌드하는 과정에서 이미지 내부에 기록 되는 것이 문제였음
### ver.2
- mlflow server는 k8s를 이용하여 실행시켰기 때문에 해당 s3 credential을 secret을 만드는 것과 envFrom으로 해결할 수 있었다. 이것으로 docker image 내부에는 s3 credential이 남지 않게 되었다.
- 그리고 이 과정에서 dockerfile을 빌드 및 실행하는 과정에서 env 설정이 잘못 되어 있다는 것을 확인하게 되었고(docker image에서 `ENV MLFLOW_S3_ENDPOINT_URL=~`  명령어로 s3 url이 minio로 잡혀있는 것을 알지 못했음) mlflow 스크립트는 잘못이 없다는 것을 확인할 수 있었다.(ㅜㅜ) 그래서 docker file에서 env 설정을 제대로 하여 mlflow 스크립트 수정 없이 s3 에 접근할 수 있게 됐다.

# Jenkins
-  github과 연동하여 Dockerfile을 빌드하는 작업을 수행하려고 함
## 발생한 문제와 해결
- jenkins 사용시 user가 jenkins 혹은 root로 되어있어 ssh 통신을 하려고 할 때, key file 위치 지정이 잘 못 되는 듯 하다. 그래서 `ssh-agent` 를 사용하여 해당 key 내용을 memory에 올려 제대로 통신할 수 있도록 하였다.

# Argo CD
- argo cd로 katib experiment를 배포, 실행시키려고 했음
## 발생한 문제와 해결
- argo cd로는 해당 katib experiment가 언제 종료되는지 알기 힘들었고, 대안으로 argo workflow를 이용했다. 그리고 해당 workflow에서 template의 성공 종료, 실패 종료 조건을 `successCondition` 으로 지정할 수 있다. 이것으로 katib experiment가 종료되는 조건을 넣어 이후 slack API를 이용해 slack으로 종료 메세지를 보내도록 workflow를 작성하였다.
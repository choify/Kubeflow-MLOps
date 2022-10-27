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
### ver.1
- jenkins 사용시 user가 jenkins 혹은 root로 되어있어 ssh 통신을 하려고 할 때, key file 위치 지정이 잘 못 되는 듯 하다. 그래서 `ssh-agent` 를 사용하여 해당 key 내용을 memory에 올려 제대로 통신할 수 있도록 하였다.
### ver.2
- jenkins 사용시 추가적인 리소스 소모가 필요하다는 문제가 있어 해당 문제를 해결하기 위해 다른 CI툴로 github actions를 사용했다.

# Argo CD
- argo cd로 katib experiment를 배포, 실행시키려고 했음
## 발생한 문제와 해결
- argo cd로는 해당 katib experiment가 언제 종료되는지 알기 힘들었고, 대안으로 argo workflow를 이용했다. 그리고 해당 workflow에서 template의 성공 종료, 실패 종료 조건을 `successCondition` 으로 지정할 수 있다. 이것으로 katib experiment가 종료되는 조건을 넣어 이후 slack API를 이용해 slack으로 종료 메세지를 보내도록 workflow를 작성하였다.

# DVC
- DVC에서 remote storage를 사용하는 경우 해당 storage에 접근하기 위해서 필요한 credential을 config에 바로 넣는 것 보다 깃에 올라가지 않는 local config에 설정하도록 한다.
- 보다 확실한 방법은 aws cli를 설치하여 해당 configure로 읽어오도록 하는 것으로 aws cli를 설치하여 s3 credential을 configure에 입력해줬다.

# Katib
- katib experiment를 수행하기 위해서는 해당 모델을 학습하는 docker image가 필요하다.
-  실험을 위한 새로운 이미지를 build 했다면 katib가 해당 모델을 학습할 때 metric을 읽어올 metrics collector 를 지정해줘야 한다. stdout, file 등 여러 소스에서 읽어올 수 있으며 본 프로젝트를 진행할 때는 stdout에서 metric을 읽어오도록 하였다.
## 발생한 문제와 해결
- katib experiment의 default metrics fotmat은 `([\w|-]+)\s*=\s*([+-]?\d*(\.\d+)?([Ee][+-]?\d+)?)`  으로 metric 이름과 value 사이에 `=` 이 오도록 되어있다. 그런데 프로젝트에서 사용한 xgboost의 stdout format은 `:` 으로  metric 이름과 value를 쌍을 짓기 때문에 katib의 metric format을 `([\\w|-]+)\\s*:\\s*([+-]?\\d*(\\.\\d+)?([Ee][+-]?\\d+)?)` 로 수정할 필요가 있었다.
- 또한 katib experimet가 실험 과정을 제대로 로깅하기 위해서는 각 stdout이 시간으로 시작해야하며 해당 시간은 isoformat이어야 한다. 그러나 xgboost는 각 metric을 출력할 때 시간을 같이 출력하지 않아서 xgboost의 monitor callback 함수를 수정하여 각 metric 출력마다 시간을 같이 출력하도록 코드를 수정하였다.
## 미해결 문제
- katib 실험용 이미지를 빌드 할 때, S3에서 데이터를 불러오는 함수를 작성했다. 그런데 이렇게 이미지를 작성한다면 katib 실험은 수십번 이루어질 텐데 그 때마다 s3에서 데이터를 읽어온다면 비용 측면에서 문제가 발생할 수도 있다. 따라서 image를 빌드하는데 시간이 오래걸릴수도 또 image의 크기가 커질 수도 있지만, image를 빌드할 때 그 안에 데이터를 복사하여 넣는 것이 좋지 않을까 라는 생각을 하게 되었다.

# Argo Workflow, events
- argocd 의 경우에는 해당 job이 언제 종료 되는지 찾는 것을 찾기 힘들어 argo workflow로 **katib 실험 -> 종료시 slack 메세지** 의 workflow를 작성하기로 했다.
- 해당 workflow가 실행 되는 것은 argo events와 github webhook을 연동하여, 특정 브랜치에서 merge가 발생하는 경우에만 해당 workflow가 실행되도록 하였다.
## 발생한 문제와 해결
- argo workflow는 argo 네임 스페이스에 설치되어 있고 kubeflow는 kubeflow 네임스페이스에 그리고  workflow의 실행은 kubeflow-user-exampe-com 이라는 네임스페이스에서 이루어졌다. 둘다 argo workflow를 사용하기 때문에 config map 과 권한에서 충돌이 일어나는데 처음엔 그것을 알지 못하였다.
- 그래서 kubeflow-user-exampe-com 에서 katib 실험을 실행시키는 것이 아니라 argo 네임스페이스에서 katib를 실행할 수 있도록 kubeflow에 profile을 생성하고 네임스페이스와 serviceaccount에 권한을 부여했다.
- 이후에는 workflow에서 충돌이 일어나고 해당 문제가 권한 때문에 생긴다는 것을 인지하여 RBAC으로 제대로 된 권한을 부여하고 다시 kubeflow-user-exampe-com 네임스페이스 하나에서만 kubeflow 관련 리소스를 관리할 수 있도록 되돌려놓았다.

# Seldon core
- 학습이 완료된 특정 모델을 불러와 배포하기 위해서는 모델을 불러올 initcontainer와 모델을 배포할 container를 둘다 정의해야 한다.
- container에는 직접 이미지를 빌드할 수도 있으나 보통 seldon core에서 제공하는 server를 사용한다. 본 프로젝트에서는 xgboost를 사용했기 때문에 xgboost server를 사용했다.
- 전처리기를 이용하여 들어오는 데이터를 전처리 하였다.
- combiner를 이용하여 모델을 앙상블 하였다.
## 발생한 문제와 해결
- xgboost server의 경우에는 모델명이 꼭 `.bst` 로 끝나야 한다. 그런데 mlflow의 autolog 를 사용하면 해당 모델은 `model.xgb`로 저장되기 때문에 s3에 올라가 있는 모델의 이름을 변경해야하는 작업이 필요했다. 
## 미해결 문제
- locust를 활용해 auto scaling이 가능한지 확인하려 했으나 맘대로 잘 되지 않았다. 서버 부하를 늘리면 그대로 서버가 터져버리기 일쑤였다. 
- 만든 모델로 inference를 수행하는 경우여서 그런 것인지, 전처리기와 combiner를 사용해서 네트워크를 거치기 때문에 해당 부분에서 병목현상이 발생하게 되는 것인지 잘 알 수 없었다.
- 그러나 inference를 담당하는 pod의 리소스 소모가 급격하게 증가하는 것으로 보아 inference를 수행하는 부분에 문제가 있는 듯 싶다.
- autoscale이 되지 않는다 하더라도 replica가 여러개인 경우에 load가 분산될 줄 알았는데 그렇지도 않았고 traffic을 나눠도 제대로 되지 않았다. seldon core에서 load balancing 하는 부분을 다시 봐야할 것 같다.

# Promethus, Grafana
- 서버 메트릭과 모델 메트릭을 측정하기 위하여 사용했다.
## 미해결 문제
- promQL을 알지 못하여서 모델 API에서 어떤 값을 불러와야 모델 메트릭을 측정할 수 있는지 알지 못하였다. 그래서 model metric을 측정하는 것을 수행하지는 못하였다.
- 서버 메트릭의 경우에도 inference를 많이 요청하는 경우 500번대 에러가 발생하는 경우가 꽤 있었는데 해당 에러를 잡지 못하는 문제가 있었다. 이 또한 promQL과 grafana dashboard를 작성하는 법을 알아야 해결할 수 있을 것 같다.
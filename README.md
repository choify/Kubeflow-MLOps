# startup-project
이어드림 스쿨 2기 과정 중 진행한 스타트업 연계 프로젝트에 대한 내용임

- 주제 : 빅데이터 분석 프레임워크 구축
- 기간 : 2022/09/05 ~ 2022/10/21
- 역할 : 구글에서 정의한 MLOps level 2를 만족하는 MLOps 파이프라인 구축

## 발표 자료
- [기획안](https://docs.google.com/presentation/d/1g8TlGWvKnN1AuEqA5nkjA-NIPwLQYDyk/edit?usp=sharing&ouid=118253427836564636716&rtpof=true&sd=true)
- [중간 발표](https://docs.google.com/presentation/d/1m8EF5LbnHuOY3mnhSsFTEKkyB3cQIyCe/edit?usp=sharing&ouid=118253427836564636716&rtpof=true&sd=true)
- [최종 발표](https://docs.google.com/presentation/d/1BbtlxzXMZAAFppnBjJYfnrecRzcd9GTB/edit?usp=sharing&ouid=118253427836564636716&rtpof=true&sd=true)

## 최종 아키텍처

![최종 아키텍처](/images/final_architecture.png)

# 타임 라인

<details>
<summary>세부 내용</summary>
<div markdown="1">

## 기획안(09/05 ~ 09/23)

### 진행 작업
-  쿠버네티스 환경을 구축해본 경험이 없기 때문에 모두의 MLOps를 참고하여 환경을 구축하였음
-  remote storage, model registry로 amazon S3를 사용하기 위해 환경을 바꾸는 작업을 수행
-  CI/CD 툴을 사용해본 적이 없기 때문에 Jenkins와 Argo CD를 이용한 CI/CD 환경을 구축해봄(ml 파이프라인에 적용해보지는 않고 되는지만 확인해봄)

### 문제점
- [MLflow 설정시 발생한 문제(ver.1)](/pj_env/troubles.md#mlflow)
- [Jenkins 사용시 발생한 문제(ver.1)](/pj_env/troubles.md#jenkins)
- [Argo CD 사용시 발생한 문제](/pj_env/troubles.md#argo-cd)

## 중간 발표(09/26~10/07)

### 진행 작업
- 두 개의 자동화 라인을 구상함
	1. 새로운 데이터가 올라오면 실험까지 자동화 하는 라인
	2. 배포를 위한 모델 학습과 모델의 배포 까지 자동화 하는 라인
- 1번 라인을 위해서 필요한 툴들 체크해봄
	- DVC
	- katib experiment 를 위한 image
	- argo workflow
	- argo event
	- jenkins
	- slack API
- 2번 라인을 위해서 필요한 것
	- mlflow
	- seldon core
	- argo cd
	- prometheus
	- grafana

### 문제점
- [DVC 사용시 발생한 문제](/pj_env/troubles.md#dvc)
- [katib 사용시 발생한 문제](/pj_env/troubles.md#katib)
- [Jenkins 사용시 발생한 문제(ver.2)](/pj_env/troubles.md#jenkins)
- [Argo Workflow 사용시 발생한 문제](/pj_env/troubles.md#argo-workflow-events)
- [Seldon core 사용시 발생한 문제](/pj_env/troubles.md#seldon-core)

## 최종 발표(10/10 ~ 10/21)

### 진행 작업
- 실제로 두 자동화 라인을 제대로 빌드하고 라인들이 제대로 실행되는지 체크

	1.  새로운 데이터가 올라오면 실험까지 자동화 하는 라인
		-   데이터 버전 관리를 git과 같이 하기 위해서 DVC를 이용하고 remote storage로 amazon s3를 사용한다.
		-   바뀐 데이터를 push하면 github actions를 이용하여 바뀐 데이터에 대한 학습을 하는 docker image를 build, push하게 한다. 그리고 데이터가 업데이트되고 해당 내용으로 katib 실험을 진행할 수 있음을 알리기 위해서 PR을 생성한다.
		-   업데이트된 학습의 PR이 merge되면 github webhook과 argo events를 이용하여 katib experiment을 실행하고 해당 실험이 끝나면 slack API를 이용하여 알람을 보내는 workflow를 실행시킨다.

	2. 배포를 위한 모델 학습과 모델의 배포 까지 자동화 하는 라인
		-  실험에서 최적의 파라미터를 선택하여 해당 모델을 mlflow server에 업로드한다. 이때 모델 저장소로 amazon s3를 사용합니다.
		-   이후 바뀐 모델에 대한 seldon core manifest 파일을 github에 push하게 합니다.
		-  argo CD는 해당 github repository와 branch 감시하고 내용이 업데이트 되면, 해당 manifest 파일을 pull하여 모델 API의 배포가 지속적으로 이루어지도록 배포를 업데이트 한다.
		- prometheus와 grafana로 해당 모델 서버와 모델의 metric을 측정한다.

### 문제점
- [Seldon core 미해결 문제](/pj_env/troubles.md#seldon-core)
- [Prometheus 미해결 문제](/pj_env/troubles.md#promethus-grafana)
</div>
</details>

## 프로젝트 진행 시 문제점
- CI/CD 툴에 대한 사용 경험 없음
- 도커 및 쿠버네티스에 익숙하지 않음
	- 환경 구축하는데 있어 엄청난 양의 에러와 부딪히게 되었고 해당 에러를 해결하는데 상당한 시간이 소요됨

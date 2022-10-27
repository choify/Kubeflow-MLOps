# startup-project
이어드림 스쿨 2기 과정 중 진행한 스타트업 연계 프로젝트에 대한 내용임

- 주제 : 빅데이터 분석 프레임워크 구축
- 기간 : 2022/09/05 ~ 2022/10/21
- 역할 : 구글에서 정의한 MLOps level 2를 만족하는 MLOps 파이프라인 구축

[기획안](https://docs.google.com/presentation/d/1g8TlGWvKnN1AuEqA5nkjA-NIPwLQYDyk/edit?usp=sharing&ouid=118253427836564636716&rtpof=true&sd=true)
[중간 발표](https://docs.google.com/presentation/d/1m8EF5LbnHuOY3mnhSsFTEKkyB3cQIyCe/edit?usp=sharing&ouid=118253427836564636716&rtpof=true&sd=true)
[최종 발표](https://docs.google.com/presentation/d/1BbtlxzXMZAAFppnBjJYfnrecRzcd9GTB/edit?usp=sharing&ouid=118253427836564636716&rtpof=true&sd=true)

## 기획안(09/05 ~ 09/23)

### 진행 작업
-  쿠버네티스 환경을 구축해본 경험이 없기 때문에 모두의 MLOps를 참고하여 환경을 구축하였음
-  remote storage, model registry로 amazon S3를 사용하기 위해 환경을 바꾸는 작업을 수행
-  CI/CD 툴을 사용해본 적이 없기 때문에 Jenkins와 Argo CD를 이용한 CI/CD 환경을 구축해봄(ml 파이프라인에 적용해보지는 않고 되는지만 확인해봄)

### 문제점
- [[troubles#MLflow|MLflow 설정시 발생한 문제]]
- [[troubles#Jenkins|Jenkins 사용시 발생한 문제]]
- [[troubles#Argo CD|Argo CD 사용시 발생한 문제]]

## 중간 발표(09/26~10/07)

### 진행 작업
- 


## 프로젝트 진행 시 문제점
- CI/CD 툴에 대한 사용 경험 없음
- 도커 및 쿠버네티스에 익숙하지 않음
	- 환경 구축하는데 있어 엄청난 양의 에러와 부딪히게 되었고 해당 에러를 해결하는데 상당한 시간이 소요됨


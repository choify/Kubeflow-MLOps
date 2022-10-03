pipeline {
    agent any
    environment {
        DOCKERHUB_USERNAME = "hahajong"
        APP_NAME = "startup-pj-demo"
        IMAGE_TAG = "${BUILD_NUMBER}"
        IMAGE_NAME = "${DOCKERHUB_USERNAME}" + "/" + "${APP_NAME}"
        REGISTRY_CREDS = 'dockerhub'
    }
    stages {
        stage('Cleanup Workspace'){
            steps {
                script {
                    cleanWs()
                }
            }
        }
        stage('Checkout SCM'){
            steps {
                git credentialsId: '555f0ca5-f98e-44ea-a862-2b9bd5c82f6b', 
                url: 'git@github.com:Hahajongsoo/startup-progject-demo.git',
                branch:'master'
            }
        }
        stage('Updating Train.py file'){
            steps {
                sh "cat train.py"
                sh "bash ./change-data-path.sh"
                sh "cat train.py"
            }
        }
        stage('Build Docker Image'){
            steps {
                script{
                    docker_image = docker.build "${IMAGE_NAME}"
                }
            }
        }
        stage('Push Docker Image'){
            steps {
                script{
                    docker.withRegistry('', REGISTRY_CREDS){                        
                        docker_image.push("${BUILD_NUMBER}")
                        docker_image.push('latest')
                    }
                }
            }
        }
        stage('Delete Docker Image'){
            steps {
                sh "docker rmi ${IMAGE_NAME}:${IMAGE_TAG}"
                sh "docker rmi ${IMAGE_NAME}:latest"
            }
        }
        stage('Push the changed train.py file to Git'){
            steps {
                script {
                    sh """
                    eval "\$(ssh-agent -s)"
                    ssh-add /var/lib/jenkins/.ssh/id_rsa_deploy-test
                    git config --global user.name "Hahajongsoo"
                    git config --global user.email "gkwhdtn95051@gmail.com"
                    git add train.py
                    git commit -m 'modifying train.py'
                    git push git@github.com:Hahajongsoo/startup-progject-demo.git master"""
                }
            }
        }
    }
}



// stage('Build Docker Image'){
//             steps {
//                 sh "docker build -t ${IMAGE_NAME}:${IMAGE_TAG} ."
//                 sh "docker build -t ${IMAGE_NAME}:latest ."
//             }
//         }
//         stage('Push Docker Image'){
//             steps {
//                 withCredentials([usernamePassword(credentialsId: 'dockerhub', passwordVariable: 'pass', usernameVariable: 'user')]) {
//                     sh "docker login -u $user --password $pass"
//                     sh "docker push -t ${IMAGE_NAME}:${IMAGE_TAG} ."
//                     sh "docker push -t ${IMAGE_NAME}:latest ."
//                 }
//             }
//         }
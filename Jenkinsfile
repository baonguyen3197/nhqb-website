pipeline {
    agent {
        kubernetes {
            label 'kaniko'
            yaml '''
kind: Pod
spec:
  containers:
  - name: kaniko
    image: gcr.io/kaniko-project/executor:debug
    imagePullPolicy: Always
    command:
    - sleep
    args:
    - 9999999
    volumeMounts:
      - name: jenkins-docker-cfg
        mountPath: /kaniko/.docker
  volumes:
  - name: jenkins-docker-cfg
    projected:
      sources:
      - secret:
          name: regcred
          items:
            - key: .dockerconfigjson
              path: config.json
'''
        }
    }

    environment {
        DOCKER_IMAGE = 'index.docker.io/nhqb3197/nhqb-mysite:latest'
        GITHUB_CREDENTIALS_ID = 'nhqb-website' // Ensure this matches the ID of your GitHub credentials in Jenkins
        DOCKER_CREDENTIALS_ID = 'dockerhub-creds'
        PATH = "/busybox:$PATH"
    }

    stages {
        stage('Checkout') {
            steps {
                // Checkout the code from your repository using the specified credentials
                git branch: 'main', credentialsId: "${GITHUB_CREDENTIALS_ID}", url: 'https://github.com/baonguyen3197/nhqb-website.git'
            }
        }

        stage('Build and Push Docker Image with Kaniko') {
            steps {
                container('kaniko') {
                    script {
                        // Run Kaniko to build and push the Docker image
                        sh '''
                        /kaniko/executor --dockerfile=/workspace/nhqb-website/Dockerfile \
                                         --context=dir:///workspace/nhqb-website/ \
                                         --destination=${DOCKER_IMAGE}
                        '''
                    }
                }
            }
        }

        // Uncomment and adjust the following stage if you need to deploy the Docker container
        // stage('Deploy') {
        //     steps {
        //         script {
        //             // Deploy the Docker container (this is an example, adjust as needed)
        //             sh 'docker run -d -p 8000:8000 ${DOCKER_IMAGE}'
        //         }
        //     }
        // }
    }

    post {
        always {
            // Clean up Docker images to save space
            sh 'docker rmi ${DOCKER_IMAGE} || true'
        }
    }
}
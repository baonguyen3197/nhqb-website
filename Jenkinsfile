pipeline {
    agent {
        kubernetes {
            label 'kaniko'
            defaultContainer 'jnlp'
            yaml """
apiVersion: v1
kind: Pod
metadata:
  labels:
    some-label: kaniko
spec:
  containers:
  - name: kaniko
    image: gcr.io/kaniko-project/executor:debug
    command:
    - sleep
    args:
    - 60
    volumeMounts:
    - name: kaniko-secret
      mountPath: /kaniko/.docker
  restartPolicy: Never
  volumes:
  - name: kaniko-secret
    secret:
      secretName: dockercred
      items:
      - key: .dockerconfigjson
        path: config.json
"""
        }
    }

    environment {
        DOCKER_IMAGE = 'nhqb3197/nhqb-mysite:latest'
        GITHUB_CREDENTIALS_ID = 'nhqb-website' // Ensure this matches the ID of your GitHub credentials in Jenkins
        DOCKER_CREDENTIALS_ID = 'dockerhub-creds'
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
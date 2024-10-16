// pipeline {
//     agent any

//     environment {
//         DOCKER_IMAGE = 'nhqb3197/nhqb-mysite:latest'
//         GITHUB_CREDENTIALS_ID = 'nhqb-website' // Ensure this matches the ID of your GitHub credentials in Jenkins
//         DOCKER_CREDENTIALS_ID = 'dockerhub-creds'
//         KANIKO_SERVICE_URL = 'http://10.10.100.90:32007'
//     }

//     stages {
//         stage('Checkout') {
//             steps {
//                 // Checkout the code from your repository using the specified credentials
//                 git branch: 'main', credentialsId: "${GITHUB_CREDENTIALS_ID}", url: 'https://github.com/baonguyen3197/nhqb-website.git'
//             }
//         }

//         stage('Build Docker Image with Kaniko') {
//             steps {
//                 script {
//                     // Define the Kaniko build command
//                     def kanikoBuildCommand = """
//                     curl -X POST ${KANIKO_SERVICE_URL}/build \
//                         -H 'Content-Type: application/json' \
//                         -d '{
//                             "dockerfile": "./Dockerfile",
//                             "context": "dir://workspace/",
//                             "destination": "nhqb3197/nhqb-mysite:latest"
//                         }'
//                     """

//                     // Execute the Kaniko build command
//                     sh kanikoBuildCommand
//                 }
//             }
//         }

//         // stage('Deploy') {
//         //     steps {
//         //         script {
//         //             // Deploy the Docker container (this is an example, adjust as needed)
//         //             sh 'docker run -d -p 8000:8000 $DOCKER_IMAGE'
//         //         }
//         //     }
//         // }
//     }

//     // post {
//     //     always {
//     //         // Clean up Docker images to save space
//     //         sh 'docker rmi $DOCKER_IMAGE || true'
//     //     }
//     // }
// }

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
    image: gcr.io/kaniko-project/executor:latest
    command:
    - /busybox/sh
    args:
    - -c
    - "while true; do sleep 30; done;"
    volumeMounts:
    - name: kaniko-secret
      mountPath: /kaniko/.docker
    - name: dockerfile-storage
      mountPath: /workspace
  volumes:
  - name: kaniko-secret
    secret:
      secretName: regcred
      items:
      - key: .dockerconfigjson
        path: config.json
  - name: dockerfile-storage
    persistentVolumeClaim:
      claimName: kaniko-pv-claim
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
                        /kaniko/executor --dockerfile=/workspace/Dockerfile \
                                         --context=dir://workspace/ \
                                         --destination=$DOCKER_IMAGE
                        '''
                    }
                }
            }
        }

        stage('Deploy') {
            steps {
                script {
                    // Deploy the Docker container (this is an example, adjust as needed)
                    sh 'docker run -d -p 8000:8000 $DOCKER_IMAGE'
                }
            }
        }
    }

    post {
        always {
            // Clean up Docker images to save space
            sh 'docker rmi $DOCKER_IMAGE || true'
        }
    }
}
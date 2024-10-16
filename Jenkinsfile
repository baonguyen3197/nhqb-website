pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'nhqb3197/nhqb-mysite:latest'
        GITHUB_CREDENTIALS_ID = 'nhqb-website' // Ensure this matches the ID of your GitHub credentials in Jenkins
        DOCKER_CREDENTIALS_ID = 'dockerhub-creds'
        KANIKO_SERVICE_URL = 'http://10.10.100.90:32007'
    }

    stages {
        stage('Checkout') {
            steps {
                // Checkout the code from your repository using the specified credentials
                git branch: 'main', credentialsId: "${GITHUB_CREDENTIALS_ID}", url: 'https://github.com/baonguyen3197/nhqb-website.git'
            }
        }

        stage('Build Docker Image with Kaniko') {
            steps {
                script {
                    // Define the Kaniko build command
                    def kanikoBuildCommand = """
                    curl -X POST ${KANIKO_SERVICE_URL}/build \
                        -H 'Content-Type: application/json' \
                        -d '{
                            "dockerfile": "./Dockerfile",
                            "context": "dir://workspace/",
                            "destination": "nhqb3197/nhqb-mysite:latest"
                        }'
                    """

                    // Execute the Kaniko build command
                    sh kanikoBuildCommand
                }
            }
        }

        // stage('Deploy') {
        //     steps {
        //         script {
        //             // Deploy the Docker container (this is an example, adjust as needed)
        //             sh 'docker run -d -p 8000:8000 $DOCKER_IMAGE'
        //         }
        //     }
        // }
    }

    // post {
    //     always {
    //         // Clean up Docker images to save space
    //         sh 'docker rmi $DOCKER_IMAGE || true'
    //     }
    // }
}
pipeline {
    agent any

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

        stage('Build Docker Image') {
            steps {
                script {
                    // Build the Docker image
                    sh 'docker build -t $DOCKER_IMAGE .'
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                script {
                    // Log in to Docker Hub
                    sh 'echo $DOCKER_PASSWORD | docker login -u $DOCKER_USERNAME --password-stdin'
                    // Push the Docker image
                    sh 'docker push $DOCKER_IMAGE'
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
pipeline {
    // agent any
    agent {
        kubernetes {
            yamlFile 'kaniko-builder.yaml'
        }
    }

    environment {
        DOCKER_IMAGE = 'index.docker.io/nhqb3197/nhqb-mysite:latest'
        GITHUB_CREDENTIALS_ID = 'nhqb-website'
        DOCKER_CREDENTIALS_ID = 'dockerhub-creds'
        // ARGOCD_SERVER = '10.10.100.90:32007'
        ARGOCD_SERVER = 'http://argo-cd-argocd-server.argocd.svc.cluster.local'  // Use internal service
        ARGOCD_APP_NAME = 'app-web'
        ARGOCD_AUTH_TOKEN = credentials('argocd-cred')
    }

    stages {
        stage("Cleanup Workspace") {
            steps {
                cleanWs()
            }
        }

        stage("Checkout from SCM") {
            steps {
                git branch: 'main', credentialsId: "${GITHUB_CREDENTIALS_ID}", url: 'https://github.com/baonguyen3197/nhqb-website.git'
            }
        }

        // stage('Build & Push with Kaniko') {
        //     steps {
        //         container(name: 'kaniko', shell: '/busybox/sh') {
        //             sh '''#!/busybox/sh
        //             /kaniko/executor --dockerfile `pwd`/Dockerfile --context `pwd` --destination=${DOCKER_IMAGE}
        //             '''
        //         }
        //     }
        // }
        
        // stage('Build & Push Docker Image') {
        //     steps {
        //         withCredentials([usernamePassword(credentialsId: "${DOCKER_CREDENTIALS_ID}", passwordVariable: 'DOCKER_PASSWORD', usernameVariable: 'DOCKER_USERNAME')]) {
        //             sh """
        //             docker build -t ${DOCKER_IMAGE} .
        //             echo "${DOCKER_PASSWORD}" | docker login --username "${DOCKER_USERNAME}" --password-stdin
        //             docker push ${DOCKER_IMAGE}
        //             """
        //         }
        //     }
        // }

        stage('Trigger ArgoCD Sync') {
            steps {
                withCredentials([string(credentialsId: 'argocd-cred', variable: 'ARGOCD_AUTH_TOKEN')]) {
                    sh '''
                    curl -s -X POST \
                    -H "Content-Type: application/json" \
                    -H "Authorization: Bearer ${ARGOCD_AUTH_TOKEN}" \
                    ${ARGOCD_SERVER}/api/v1/applications/${ARGOCD_APP_NAME}/sync
                    '''
                }
            }
        }
    }
}
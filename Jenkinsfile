// pipeline {
//     agent {
//         kubernetes {
//             label 'kaniko'
//             yaml '''
// kind: Pod
// metadata:
//   labels:
//     app: jenkins-agent
// spec:
//   containers:
//   - name: jnlp
//     image: jenkins/inbound-agent:latest
//     imagePullPolicy: Always
//     env:
//     - name: JENKINS_URL
//       value: http://10.10.100.90:32050  # Jenkins master URL with NodePort for web interface
//   - name: kaniko
//     image: gcr.io/kaniko-project/executor:debug
//     imagePullPolicy: Always
//     command:
//     - sleep
//     args:
//     - 9999999
//     volumeMounts:
//       - name: workspace-volume
//         mountPath: /workspace
//   volumes:
//   - name: workspace-volume
//     emptyDir: {}
// '''
//         }
//     }

//     environment {
//         DOCKER_IMAGE = 'index.docker.io/nhqb3197/nhqb-mysite:latest'
//         GITHUB_CREDENTIALS_ID = 'nhqb-website' // Ensure this matches the ID of your GitHub credentials in Jenkins
//         DOCKER_CREDENTIALS_ID = 'dockerhub-creds'
//         PATH = "/busybox:$PATH"
//     }

//     stages {
//         stage('Checkout') {
//             steps {
//                 // Checkout the code from your repository using the specified credentials
//                 git branch: 'main', credentialsId: "${GITHUB_CREDENTIALS_ID}", url: 'https://github.com/baonguyen3197/nhqb-website.git'
//             }
//         }

//         stage('Build and Push Docker Image with Kaniko') {
//             steps {
//                 container('kaniko') {
//                     script {
//                         // Run Kaniko to build and push the Docker image
//                         sh '''
//                         /kaniko/executor --dockerfile=/workspace/agent/remoting/Dockerfile \
//                                          --context=dir:///workspace \
//                                          --destination=${DOCKER_IMAGE}
//                         '''
//                     }
//                 }
//             }
//         }

//         // Uncomment and adjust the following stage if you need to deploy the Docker container
//         // stage('Deploy') {
//         //     steps {
//         //         script {
//         //             // Deploy the Docker container (this is an example, adjust as needed)
//         //             sh 'docker run -d -p 8000:8000 ${DOCKER_IMAGE}'
//         //         }
//         //     }
//         // }
//     }

//     post {
//         always {
//             // Clean up Docker images to save space
//             sh 'docker rmi ${DOCKER_IMAGE} || true'
//         }
//     }
// }

pipeline {

  agent {
    kubernetes {
      yamlFile 'kaniko-builder.yaml'
    }
  }

  environment {
        APP_NAME = "nhqb-mysite"
        RELEASE = "1.0.0"
        DOCKER_USER = "nhqb3197"
        DOCKER_PASS = 'Therookie97!'
        IMAGE_NAME = "${DOCKER_USER}" + "/" + "${APP_NAME}"
        IMAGE_TAG = "${RELEASE}-${BUILD_NUMBER}"
        /* JENKINS_API_TOKEN = credentials("JENKINS_API_TOKEN") */

    }

  stages {

    stage("Cleanup Workspace") {
      steps {
        cleanWs()
      }
    }

    stage("Checkout from SCM"){
            steps {
                git branch: 'main', credentialsId: 'github', url: 'https://github.com/baonguyen3197/nhqb-website.git'
            }

        }

    stage('Build & Push with Kaniko') {
      steps {
        container(name: 'kaniko', shell: '/busybox/sh') {
          sh '''#!/busybox/sh

            /kaniko/executor --dockerfile `pwd`/Dockerfile --context `pwd` --destination=${IMAGE_NAME}:${IMAGE_TAG} --destination=${IMAGE_NAME}:latest
          '''
        }
      }
    }
  }
}
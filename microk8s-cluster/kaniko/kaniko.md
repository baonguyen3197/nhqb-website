## --- docker-serect --- ##
microk8s kubectl create secret docker-registry regcred \
    --docker-server=https://index.docker.io/v1/ \
    --docker-username={username} \
    --docker-password={password} \
    --docker-email={email}
    -n devops-tools

## --- kaniko --- ##
using kaniko to build image without docker inside the jenkins pipeline


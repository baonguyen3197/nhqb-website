## --- docker-serect --- ##
microk8s kubectl create secret docker-registry regcred \
    --docker-server=https://index.docker.io/v1/ \
    --docker-username=nhqb3197 \
    --docker-password=Therookie97! \
    --docker-email=baonguyen3197@gmail.com
    - n devops-tools

## --- kaniko --- ##
using kaniko to build image without docker inside the jenkins pipeline


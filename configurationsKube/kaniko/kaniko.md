## --- docker-serect --- ##
microk8s kubectl create secret docker-registry regcred \
    --docker-server=https://index.docker.io/v1/ \
    --docker-username=nhqb3197 \
    --docker-password=Therookie97! \
    --docker-email=baonguyen3197@gmail.com
    - n devops-tools

## --- kaniko --- ##
nhqb-vm-1
path: /home/nhqb/Desktop/devops-tools/kaniko

microk8s kubectl apply -f pvc.yaml
microk8s kubectl apply -f pv.yaml
microk8s kubectl apply -f deployment.yaml
microk8s kubectl apply -f service.yaml

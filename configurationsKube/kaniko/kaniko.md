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

microk8s kubectl apply -f volume.yaml
microk8s kubectl apply -f volume-claim.yaml
microk8s kubectl apply -f inspect.yaml
microk8s kubectl apply -f pod.yaml
microk8s kubectl apply -f service.yaml

## --- list files --- ##
ls -a

.. deployment.yaml  Dockerfile  inspect.yaml  pod.yaml  volume-claim.yaml  volume.yaml

## add Dockerfile to build image of kaniko
## inspect.yaml to check the inside of the container


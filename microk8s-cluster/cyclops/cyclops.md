microk8s helm repo add cyclops-ui https://cyclops-ui.com/helm
microk8s helm repo update

microk8s helm install cyclops \
--namespace cyclops \
--create-namespace \
cyclops-ui/cyclops

microk8s kubectl get pods -n cyclops
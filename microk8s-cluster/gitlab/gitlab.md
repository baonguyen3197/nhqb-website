# Install GitLab on MicroK8s Cluster
microk8s helm repo add gitlab https://charts.gitlab.io/

microk8s helm install gitlab gitlab/gitlab
  --set postgresql.install=false
  --set global.psql.host=10.0.30.51,10.0.10.52,10.0.20.58
  --set global.psql.port=5433
  --set global.psql.password.secret=gitlab-yb-password
  --set global.psql.password.key=yb-password

# Get initial root password for GitLab
microk8s kubectl get secret gitlab-gitlab-initial-root-password -ojsonpath='{.data.password}' | base64 --decode ; echo

# Set up password secret for GitLab
microk8s kubectl create secret generic gitlab-yb-password \
  --from-literal=yb-password=$(openssl rand -base64 32)

# Get password secret for GitLab
microk8s kubectl get secret gitlab-yb-password -o jsonpath="{.data.yb-password}" | base64 --decode

# Deploy Gitlab
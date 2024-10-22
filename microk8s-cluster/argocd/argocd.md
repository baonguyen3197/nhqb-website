## --- Get the password for the ArgoCD UI --- ##

```bash
microk8s kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 --decode
```

## --- Access the ArgoCD UI --- ##

expose node port 32007 for http and 32443 for https in service.yaml

## --- Create the service --- ##

apply the argocd-mediago-webapp.yaml to create the service


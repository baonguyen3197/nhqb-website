## --- Get the password for the ArgoCD UI --- ##

```bash
microk8s kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 --decode
```

## --- Create the service --- ##

apply the argocd-mediago-webapp.yaml to create the service

## --- Create the ingress --- ##

```bash
microk8s kubectl apply -f argocd-ingress.yaml
``` 

## --- Edit the argocd-server deployment to allow insecure connections --- ##

```bash
microk8s kubectl -n argocd edit deploy argo-cd-argocd-server
``` 

Find the `containers` section and add the following:

```yaml
containers:
        - name: server
          image: quay.io/argoproj/argocd:v2.7.2
          args:
            - /usr/local/bin/argocd-server
            - '--port=8080'
            - '--metrics-port=8083'
            - '--insecure' # Add this line to allow insecure connections
```

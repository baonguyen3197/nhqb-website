## --- Install ngrok --- ##
```bash

microk8s helm repo add ngrok https://charts.ngrok.com

export NGROK_AUTHTOKEN={AUTHTOKEN}
export NGROK_API_KEY={API_KEY}

microk8s kubectl create secret generic ngrok-credentials \
  --from-literal=apiKey=$NGROK_API_KEY \
  --from-literal=authtoken=$NGROK_AUTHTOKEN \
  --namespace ngrok-operator

microk8s helm install ngrok-operator ngrok/ngrok-operator \
	--namespace ngrok-operator \
	--create-namespace \
	--set credentials.apiKey=$NGROK_API_KEY \
	--set credentials.authtoken=$NGROK_AUTHTOKEN
```

## --- Configure ngrok --- ##
```bash
microk8s kubectl apply -f ngrok.yml
```


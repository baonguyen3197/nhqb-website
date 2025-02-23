### --- Servers --- ###

nhqb-gms-intern: 10.10.100.80
nhqb-vm-1: 10.10.100.90
nhqb-vm-2: 10.10.100.95

## --- NodePort --- ##

nhqb-vm-1: 10.10.100.90

yb-master-ui 7000 -> 32001
yb-tserver-ui 9000 -> 32005
yb-tservers 5433 -> 32006
kubernetes-dashboard 8001 -> 32002
grafana 3000 -> 32003
jenkins-service 8080 -> 32004
ingress-easyhaproxy:
    ports:
    - name: http
      protocol: TCP
      port: 80
      targetPort: 80
      nodePort: 30080
    - name: https
      protocol: TCP
      port: 443
      targetPort: 443
      nodePort: 30443
    - name: stats
      protocol: TCP
      port: 1936
      targetPort: 1936
      nodePort: 31936
argocd:
  http: 8080 -> 32007
  https: 443 -> 32443
## K8S setup

```sh
kubectl create namespace kyverno
kubectl create namespace ingress-nginx

helm install kyverno kyverno/kyverno --namespace kyverno
helm install nginx ingress-nginx/ingress-nginx --namespace ingress-nginx
```

## Deploy applications
```sh
kubectl apply -f ./deployment/good-application.yaml
kubectl apply -f ./deployment/bad-application.yaml
```

## Github Action
Prerequisite:
Settings -> Actions -> General -> Tick checkbock `Allow GitHub Actions to create and approve pull requests`

### CSV to OSCAL
```sh
python -m c2p tools csv-to-oscal-cd \
  --title "Component Definition" \
  --csv ./pipeline/component-definition.csv \
  -o ./pipeline
```

### C2P
```sh
python -m compliance_pipeline.c2p \
  -c ./pipeline/component-definition.json \
  -o ./pipeline/policy
```

### Apply Policies
```sh
find ./pipeline/policy -name '*.yaml' | while read file
do
  kubectl apply -f $file
done
```

### Collect Policy Reports
```sh
kubectl get policyreports.wgpolicyk8s.io -o yaml > ./pipeline/policyreports.wgpolicyk8s.io.yaml
python -m compliance_pipeline.p2c \
  -c ./pipeline/component-definition.json \
  -polr ./pipeline/policyreports.wgpolicyk8s.io.yaml > ./pipeline/assessment-results.json
python -m c2p tools viewer \
  -ar ./pipeline/assessment-results.json \
  -cdef ./pipeline/component-definition.json \
  -o ./pipeline/assessment-results.md
```

## After enforcement
```sh
kubectl annotate ingress bad-application redeploy=true --overwrite
sleep 30
kubectl get policyreports.wgpolicyk8s.io -o yaml > ./pipeline/policyreports.wgpolicyk8s.io.yaml
python -m compliance_pipeline.p2c \
  -c ./pipeline/component-definition.json \
  -polr ./pipeline/policyreports.wgpolicyk8s.io.yaml > ./pipeline/assessment-results.json
python -m c2p tools viewer \
  -ar ./pipeline/assessment-results.json \
  -cdef ./pipeline/component-definition.json \
  -o ./pipeline/assessment-results.md
```

## Remove policies and applications
```sh
find ./pipeline/policy -name '*.yaml' | while read file
do
  kubectl delete -f $file
done
```
```sh
kubectl delete -f ./deployment
```

### Cleanup
```sh
helm uninstall --no-hooks -n kyverno
helm uninstall --no-hooks -n nginx
```
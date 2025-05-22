## GitHub Action
```
python -m c2p tools csv-to-oscal-cd \
  --title "Component Definition" \
  --csv ./pipeline/component-definition.csv \
  -o ./pipeline
```

```
python -m compliance_pipeline.c2p \
  -c ./pipeline/component-definition.json \
  -o ./pipeline/policy
```

## K8S setup

```sh
kubectl create namespace kyverno
kubectl create namespace ingress-nginx

helm install kyverno kyverno/kyverno --namespace kyverno
helm install nginx ingress-nginx/ingress-nginx --namespace ingress-nginx

kubectl apply -f ./deployment/application.yaml

find ./pipeline/policy -name '*.yaml' | while read file
do
  kubectl apply -f $file
done

kubectl get policyreports.wgpolicyk8s.io -o yaml > policyreports.wgpolicyk8s.io.yaml
```

## After remediation
```sh
kubectl apply -f ./deployment/application-remediated.yaml
kubectl get policyreports.wgpolicyk8s.io -o yaml > policyreports.wgpolicyk8s.io.yaml
```

```
python -m compliance_pipeline.p2c \
  -c ./pipeline/component-definition.json \
  -polr ./pipeline/policyreports.wgpolicyk8s.io.yaml > ./pipeline/assessment-results.json
```

### Cleanup
```sh
helm uninstall --no-hooks -n kyverno
helm uninstall --no-hooks -n nginx
```
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

## GitHub Action Guide: Compliance-to-Policy (C2P) Workflow

### Prerequisite:

1. Enable GitHub Actions to create and approve pull requests (if you try at your forked repo)
  - Settings -> Actions -> General -> Tick checkbock `Allow GitHub Actions to create and approve pull requests`
1. Configure self-hosted runner of GitHub Action (please refer to [docker/self-hosted-runner/README.md](docker/self-hosted-runner/README.md))

### 1. Run C2P Action: Check Current Compliance Posture
This workflow does not trigger automatically. To run manually:

```
Actions -> C2P -> Run workflow 
```

The workflow executes the following steps:
- **Update OSCAL**: OSCAL Component Definition fromthe [CSV file](https://github.com/yana1205-kubecon-ja-2025/compliance-pipeline/blob/main/pipeline/component-definition.csv).
- **C2P (Compliance to Policy)**: Generate Kyverno Policies and apply them to your Kubernetes Cluster
- **P2C (Policy to Compliance)**:  Collects Kyverno policy reports from the cluster and produces OSCAL-formatted assessment results
- **Pull Request**: Creates a PR with all generated artifacts. The PR description summarizes your current compliance posture (e.g. https://github.com/yana1205-kubecon-ja-2025/compliance-pipeline/pull/6)

### 2. Run C2P Action: Enforce Policies
To switch from advisory to enforced policies:

1. Update the Mapping CSV
  In the [component-definition.csv](https://github.com/yana1205-kubecon-ja-2025/compliance-pipeline/blob/main/pipeline/component-definition.csv)
  - change the `$Parameter_Value_Alternatives` column from `FALSE` to `TRUE`
  - push the change to GitHub
1. Re-run the C2P GitHub Action
  - Now the new policy `enforce-tls-on-ingress` is deployed.
1. Trigger Admission for Affected Resources
  - Kyverno policies apply on admission. Re-trigger admission for bad-application Ingress:
      ```
      kubectl annotate ingress bad-application redeploy=true --overwrite
      ```
1. Confirm that the `bad-application` ingress is automatically updated to use TLS:
    
    (TODO: disallow HTTP(80) and enforce only HTTPS (443))
    
    <img width="613" alt="image" src="https://github.com/user-attachments/assets/8ff16f6f-46e2-4a0c-a755-8c3fd8d0b5b6" />

1. Re-run the C2P GitHub Action
1. The generated PR should now indicate full compliance. (e.g. https://github.com/yana1205-kubecon-ja-2025/compliance-pipeline/pull/7)

### 3. Cleanup
To reset the repository state:
1. Run the `Cleanup` GitHub Action
  This will:
  - Remove all generated artifacts (e.g., policies, assessment results)
  - Delete deployed ingresses and policies from your Kubernetes
  - Restore the original version of the `component-definition.csv`
  - Push the cleanup commit directly to the `main` branch

## Manual at CLI

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

### After enforcement
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

### Remove policies and applications
```sh
find ./pipeline/policy -name '*.yaml' | while read file
do
  kubectl delete -f $file
done
```
```sh
kubectl delete -f ./deployment
```

## Cleanup
```sh
helm uninstall --no-hooks -n kyverno
helm uninstall --no-hooks -n nginx
```
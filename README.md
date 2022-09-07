# Kind Setup
From [Kind Ingress Guide](https://kind.sigs.k8s.io/docs/user/ingress/)

```bash
kind create cluster --name demo-a --config files/kind.yml
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/kind/deploy.yaml
kubectl wait --namespace ingress-nginx \
  --for=condition=ready pod \
  --selector=app.kubernetes.io/component=controller \
  --timeout=90s
```

# Installing

```bash
pip install armada-client
```

# Running

```bash
python3 ./src/start.py

python3 ./src/cancel.py
```
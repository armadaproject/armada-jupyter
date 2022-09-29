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

```yml
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
  - role: control-plane
    image: "kindest/node:v1.21.10"
    kubeadmConfigPatches:
    - |
      kind: InitConfiguration
      nodeRegistration:
        kubeletExtraArgs:
          node-labels: "ingress-ready=true"
    extraPortMappings:
    - containerPort: 80
      hostPort: 80
      protocol: TCP
    - containerPort: 443
      hostPort: 443
      protocol: TCP

  - role: worker
    image: "kindest/node:v1.21.10"
```

# Installing

```bash
# Using pyproject.toml
pip install .
```

# Running

Set the following environment variables:

```bash
ARMADA_SERVER=localhost
ARMADA_PORT=50051
DISABLE_SSL=true
```

```bash
python3 -m armada_jupyter ./env/files/no-gpu.yml
```
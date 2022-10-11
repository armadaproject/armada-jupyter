# Armada-Jupyter

Armada Jupyter is a service for deploying JupyterLab K8s Pods onto Armada.

## Prerequisites

Please make sure you have [Armada](https://github.com/G-Research/armada) installed and running.

Ensure that the executor setting has been changed:

```yaml
kubernetes:
  podDefaults:
    ingress:
      hostnameSuffix: "domain.com"
```

Then make sure that `*.jupyter.domain.com` resolves to your k8s cluster.

## Installation

Please following the following guide:

- [Quickstart](./docs/quickstart.md)
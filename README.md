# Armada-Jupyter

Armada Jupyter is a service for submitting JupyterLab Jobs onto Armada.

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

## Cluster Preparation

Armada-Jupyter will need a cluster setup with ingress. If you are using kind, you will need to do this differently.

Please follow the [kind](./docs/kind.md) guide to setup your cluster.

## Installation

Please following the following guide:

- [Quickstart](./docs/quickstart.md)
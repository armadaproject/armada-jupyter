# Armada - Jupyter Deployment Design

## Problem Description

Armada's ability to submit jobs across clusters should be exploited to allow for the submission of per-user JupyterLab pods.

With minimal configuration changes to the Armada executor configuration, a user should be able to submit a JupyterLab pod that is accessible from their browser using a URL that is unique to them. This should all be done from one of the Armada Clients.

## Proposed Solution

Users will be able to write a configuration file for setting up the jupyterlab pod, and then submit this with a single command. A single command will also allow for cancelling the deployment.

## Current Questions

- Should we write this in Python, or Go? (Go would have a single executable, which is probably better for the end user)

## Design

### Configuration File

The configuration file will allow for:

- Control over the resources that are allocated to the pod
- Control over the image that is used for the jupyterlab pod
- Control over the timeout for the pod

In the future, we may want to allow for more configuration options, such as:

- Control over the ingress configuration (For more complex armada deployments)
- Control over the storage configuration (e.g. persistent storage)
- Control over Armada authentication (e.g. using a different authentication method)

The configuration file will be written in YAML, and will be passed to the Armada client as a command line argument.

```yml
version: "0.1"

submissions:
- name: "jupyterlab"
  image: "jupyter/tensorflow-notebook:latest"
  timeout: 36hrs
  resources:
    cpu: 1
    memory: 1Gi
```

### User Commands

The user will be able to deploy a jupyterlab pod with a single command:

```bash
armada-jupyter deploy --config config.yml
```

### Accessing the JupyterLab pod

After the deployment has been created, the user will be able to access the jupyterlab pod by visiting the URL that is printed to the console.

The console will also print the token needed to access the jupyterlab pod.

## Future Considerations

- Build custom images for setups that are common within G-Research
- Support a range of languages
- Support more than just juypterlab (e.g VSCode for C#)
- Renaming the project to something more generic (e.g. Armada Labratory, Armada Interactive)
- Support a range of authentication methods as required by GR

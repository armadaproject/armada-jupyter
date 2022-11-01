# Armada - JupyterLab Pod Design

## Problem Description

Armada's ability to submit jobs across clusters should be used to allow for the submission of per-user JupyterLab pods.

With minimal configuration changes to the Armada executor configuration, a user should be able to submit a JupyterLab pod that is accessible from their browser using a URL that is unique to them. This should all be done from one of the Armada Clients.

## Proposed Solution

Users will be able to write a configuration file for setting up the JupyterLab pod, and then submit this with a single command.

## Design

The program will be designed in Python.

### Configuration File

The configuration file will allow for:

- Control over the resources that are allocated to the pod
- Control over the image that is used for the JupyterLab pod
- Control over the timeout for the pod

In the future, we may want to allow for more configuration options, such as:

- Control over the ingress configuration (For more complex Armada deployments)
- Control over the storage configuration (e.g. persistent storage)
- Control over Armada authentication (e.g. using a different authentication method)

The configuration file will be written in YAML, and will be passed to the Armada client as a command line argument.

```yml
version: "0.1"

submissions:
- name: "jupyterlab"
  image: "jupyter/tensorflow-notebook:latest"
  timeout: 36h
  resources:
    cpu: 1
    memory: 1Gi
```

### User Commands

The user will be able to submit a JupyterLab pod with a single command:

```bash
armada-jupyter submit --config config.yml
```

### Accessing the JupyterLab pod

After a pod has been submitted, the user will be able to access the JupyterLab pod by visiting the URL that is printed to the console.

The console will also print the token needed to access the JupyterLab pod.

## Future Considerations

- Build custom images for setups that are common within G-Research
- Support a range of languages
- Support more than just JupyterLab (e.g VSCode for C#)
- Renaming the project to something more generic (e.g. Armada Labratory, Armada Interactive)
- Support a range of authentication methods as required by GR

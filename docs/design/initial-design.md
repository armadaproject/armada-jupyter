# Armada - Jupyter Deployment Design

## Problem Description

Armada's ability to deploy across clusters should be exploited to allow for the deployment of per-user JupyterLab instances.

With minimal configuration changes to the Armada chart, a user should be able to deploy a JupyterLab instance that is accessible from their browser using with a URL that is unique to them. This should all be done from one of the Armada Clients.

## Proposed Solution

Users will be able to write a configuration file for setting up the jupyterlab instance, and then deploy this with a single command. A single command will also allow for cancelling the deployment.

## Current Questions

- Should we write this in Python, or Go? (Go would have a single executable, which is probably better for the end user)
- How will we handle the authentication between the armada client and the armada server?
- How will we allow for shutting down the jupyterlab instance? We will need some way of remembering / storing armada job ID's or applying a custom label to the job.

## Design

### Configuration File

The configuration file will allow for:

- Control over the resources that are allocated to the jupyterlab instance
- Control over the image that is used for the jupyterlab instance

In the future, we may want to allow for more configuration options, such as:

- Control over the ingress configuration (For more complex armada deployments)
- Control over the storage configuration (e.g. persistent storage)
- Control over Armada authentication (e.g. using a different authentication method)

The configuration file will be written in YAML, and will be passed to the Armada client as a command line argument.

```yml
version: "0.1"

deployments:
- name: "jupyterlab"
  image: "jupyter/tensorflow-notebook:latest"
  resources:
    cpu: 1
    memory: 1Gi
```

### User Commands

The user will be able to deploy a jupyterlab instance with a single command:

```bash
armada-jupyter deploy --config config.yml
```

### Accessing the JupyterLab Instance

After the deployment has been created, the user will be able to access the jupyterlab instance by visiting the URL that is printed to the console.

The console will also print the token needed to access the jupyterlab instance.

## Future Considerations

- Build custom images for setups that are common within G-Research
- Support a range of languages
- Support more than just juypterlab (e.g VSCode for C#)
- Renaming the project to something more generic (e.g. Armada Labratory)
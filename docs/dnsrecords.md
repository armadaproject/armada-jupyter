## Domain Setup Guide

This document describes how to setup DNS records for your domain.

Armada sets up the domain as follows (As defined [here](https://github.com/G-Research/armada/blob/master/internal/executor/util/kubernetes_object.go#L95).):

`(ServicePortName)-(PodName).(Namespace).(HostnameSuffix)`

-  `HostnameSuffix` is set from the executor configuration under `hostnameSuffix`.
    This can be found [here](https://github.com/G-Research/armada/blob/master/config/executor/config.yaml#L36).
    ```yml
    podDefaults:
        ingress:
        hostnameSuffix: "svc"
    ```

-   `PodName` is determined by Armada, and not set by the user.

-   `Namespace` and `ServicePortName` are defined in the job spec. For example the following podspec:
    ```yml
    queue: default
    jobSetId: testing
    jobs:
    - priority: 1
        namespace: personal-anonymous
        podSpec:
        containers:
            - name: jupyterlab
            imagePullPolicy: IfNotPresent
            image: jupyter/tensorflow-notebook:latest
            ports:
                - containerPort: 8888
                name: jupyterlab
    ```
    Would result in the following DNS record:
    `jupyterlab-(PodName).personal-anonymous.(HostnameSuffix)`


## DNS Record Setup

For the purposes of this guide, we will set HostnameSuffix to `domain.com`

`domain.com` should point to the IP address of the Kubernetes cluster.

`*.domain.com` should also point to the IP address of the Kubernetes cluster.

If you want to have less wildcards, you can instead set wildcards for the individual namespaces.

For example: `*.<namespace>.domain.com` can point to the IP address of the Kubernetes cluster.


## Local DNS Record Setup

If you want to test this locally, you can use one of the following methods:

- Windows: https://support.4it.com.au/article/how-to-add-a-dns-entry-manually-to-a-windows-computer/
- Linux: https://www.tecmint.com/setup-local-dns-using-etc-hosts-file-in-linux/
- MacOS: https://markinns.com/archive/how-to-setup-a-local-dns-host-file-on-mac-os-x.html
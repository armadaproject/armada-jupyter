# Quickstart

## Pre-requisites

If you are using kind you will need to follow the [kind](./docs/kind.md) guide to setup your cluster.

## Set up the jupyter cluster namespace

This is the default namespace for anonymous users setup by the [localdev armada script](https://github.com/G-Research/armada/blob/master/localdev/run.sh)

```bash
kubectl create namespace personal-anonymous
```

## Install the Python Packages

```bash
python3 -m pip install --upgrade pip
python3 -m pip install .
```

## Set the following environment variables:

```bash
export ARMADA_SERVER=localhost
export ARMADA_PORT=50051
export DISABLE_SSL=true
```

## Create the Required Python Queue

An example of working with queues can be found in the [queues example](https://github.com/G-Research/armada/blob/master/client/python/examples/queues.py) in the main Armada Repo.

## Run the Armada Client

```bash
python3 -m armada_jupyter submit ./example/testing.yml

Getting Submission Objects from ./example/testing.yml
Submitting 2 Jobs to Armada
Submitted Job 01gmqjyvrvha22j4sjw1h2fv0v to Armada
Job is Queued
Job 01gmqjyvrvha22j4sjw1h2fv0v will be running at: http://jupyterlab-8888-armada-01gmqjyvrvha22j4sjw1h2fv0v-0.personal-anonymous.mydomain:8888
```

This will show the URL's that you can use to access the JupyterLab instance.

**NOTE: The Token is hardcoded as `testing`**

To change the token, change the value in the `/example/testing.yml` file.


## Accessing the JupyterLab instance

You can access the JupyterLab instance by using the URL's that are printed out by the client.

Please see the [dnsrecords documentation](./docs/dnsrecords.md) guide for more information on how to access the JupyterLab instance.

## Cancelling a Job

To cancel a job you can use the following command:

```
python3 -m armada_jupyter cancel {URL}
```

URL should be the URL returned by the submit command.

i.e https://jupyterlab-8888-armada-JOBID-0.jupyter.domain:8888
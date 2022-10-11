# Quickstart

## Pre-requisites

Please make sure you have setup the kind cluster correctly. The guide can be found [here](./kind.md).

## Set up the jupyter cluster namespace

```bash
kubectl create namespace armada
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

This script by default will create a queue called `default`

```bash
python3 ./docs/dev/gen_queue.py
```

## Run the Armada Client

```bash
python3 -m armada_jupyter ./example/testing.yml
```

## Cancelling all Jobs

**NOTE: This will kill all jobs running on queue `default` and job-set-id `testing`**

```
python3 ./docs/dev/cancel.py
```
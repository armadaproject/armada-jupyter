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
python3 -m pip install ".[test,format]"
```

## Create the Required Python Queue

This script by default will create a queue called `default`

```bash
python3 ./docs/dev/gen_queue.py
```

## Set the following environment variables:

```bash
ARMADA_SERVER=localhost
ARMADA_PORT=50051
DISABLE_SSL=true
```

## Run the Armada Client

```bash
python3 -m armada_jupyter ./example/testing.yml
```
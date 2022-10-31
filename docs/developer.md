# Developer Install

## Install Python Packages for Testing

```bash
python3 -m pip install --upgrade pip
python3 -m pip install ".[test,format]"
```

## Run Linting

```bash
tox -r -e format-code
```

## Run Tests

```bash
tox -r -e py37
```

## Running

See [Quickstart](./quickstart.md) for more information on how to run Armada-Jupyter.

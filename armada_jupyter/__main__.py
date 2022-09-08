import typer

app = typer.Typer(help="CLI for Armada Jupyter.")


@app.command()
def submit(file: str):
    """
    Creates new JupyterLab pods defined in the submission file
    """

    print(f"Submitting pods from {file}")


if __name__ == "__main__":
    app()

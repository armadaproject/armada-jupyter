import typer

app = typer.Typer(help="Awesome CLI user manager.")


@app.command()
def submit(file: str):
    """
    Creates new pods defined in the submission file
    """
    print(f"Submitting pods from {file}")


if __name__ == "__main__":
    app()

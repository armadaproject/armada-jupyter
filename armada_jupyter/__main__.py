import time

import typer
from armada_client.client import ArmadaClient

from armada_jupyter import armada, submissions
from armada_jupyter.armada import check_job_status, construct_url

app = typer.Typer(help="CLI for Armada Jupyter.")


@app.command()
def submit(file: str):
    """
    Creates new JupyterLab pods defined in the submission file
    """
    submit_worker(file, ArmadaClient)


def submit_worker(file: str, armada_client: ArmadaClient):
    """
    A worker function for submit command.

    This function is separated from submit command to allow for easier testing.
    """

    typer.echo(f"Getting Submission Objects from {file}")
    submission = submissions.convert_to_submission(file)

    typer.echo(f"Submitting {len(submission.jobs)} Jobs to Armada")

    for job in submission.jobs:

        client, job_id = armada.submit(submission, job, armada_client)
        typer.echo(f"Submitted Job {job_id} to Armada")

        # Sleep to make sure that job-set-id is created
        time.sleep(3)

        successful = check_job_status(client, submission, job_id)

        if not successful:
            typer.echo(f"Job {job_id} failed to start")

        else:
            url = construct_url(job, job_id)
            typer.echo(f"Job {job_id} started")
            typer.echo(f"URL: {url}")

    typer.echo("Completed all submissions!\n\n")


if __name__ == "__main__":
    app()

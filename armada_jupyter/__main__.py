import typer
from armada_client.typings import EventType

from armada_jupyter import armada, submissions
from armada_jupyter.constants import JOB_SET_ID

app = typer.Typer(help="CLI for Armada Jupyter.")


@app.command()
def submit(file: str):
    """
    Creates new JupyterLab pods defined in the submission file
    """

    typer.echo(f"Getting Submission Objects from {file}")
    submissions_objects = submissions.get_submissions(file)

    for submission in submissions_objects:
        typer.echo(f"Submitting [{submission.name}] to Armada")
        resp, client = armada.submit(submission)

        job_id = resp.job_response_items[0].job_id
        typer.echo(f"URL is: https://armada-{job_id}-0.jupyter.armadaproject.io")

        # complete an events loop

        terminal_events = [
            EventType.duplicate_found,
            EventType.failed,
            EventType.cancelled,
        ]

        event_stream = client.get_job_events_stream(
            queue=submission.armada_queue, job_set_id=JOB_SET_ID
        )

        # Contains all the possible message types
        for event in event_stream:

            event = client.unmarshal_event_response(event)
            if event.message.job_id == job_id:
                if event.type == EventType.running:
                    typer.echo("\nJob is running!")
                    print(event)
                    return
                elif event.type in terminal_events:
                    typer.echo(f"Job {job_id} failed to start")
                    return

        typer.echo("Completed all submissions!")


if __name__ == "__main__":
    app()

import typer
from armada_client.typings import EventType

from armada_jupyter import armada, submissions

app = typer.Typer(help="CLI for Armada Jupyter.")


@app.command()
def submit(file: str):
    """
    Creates new JupyterLab pods defined in the submission file
    """

    typer.echo(f"Getting Submission Objects from {file}")
    submission = submissions.convert_to_submission(file)

    resp, client, no_of_jobs = armada.submit(submission)
    typer.echo(f"Submitting {no_of_jobs} Jobs to Armada")

    job_id = resp.job_response_items[0].job_id
    typer.echo(f"URL is: https://armada-{job_id}-0.jupyter.armadaproject.io")

    # complete an events loop

    terminal_events = [
        EventType.duplicate_found,
        EventType.failed,
        EventType.cancelled,
        EventType.succeeded,
    ]

    event_stream = client.get_job_events_stream(
        queue=submission.queue, job_set_id=submission.job_set_id
    )

    jobs_submitted = 0

    # Checks that all the jobs have started.
    # If any of the terminal events are received,
    # this means it has failed to start correctly, including
    # if it "succeeded"
    for event in event_stream:

        event = client.unmarshal_event_response(event)
        if event.message.job_id == job_id:
            if event.type == EventType.running:
                typer.echo("\nJob is running!")
                print(event)
                jobs_submitted += 1

            elif event.type in terminal_events:
                typer.echo(f"Job {job_id} failed to start")
                jobs_submitted += 1

        if jobs_submitted == no_of_jobs:
            break

    typer.echo("Completed all submissions!")


if __name__ == "__main__":
    app()

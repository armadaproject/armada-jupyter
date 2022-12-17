import os

import grpc
from armada_client.client import ArmadaClient


def cancel_jobset(client):
    """
    Submits and Cancels Jobs by two different methods:
    - Cancelling a job by its job id
    - Cancelling a job by its job set id
    """

    job_set_id = "testing"
    queue = "default"

    # This job is cancelled using the queue and job_set
    client.cancel_jobs(queue=queue, job_set_id=job_set_id)


def cancel():

    # Ensures that the correct channel type is generated
    if DISABLE_SSL:
        channel = grpc.insecure_channel(f"{HOST}:{PORT}")
    else:
        channel_credentials = grpc.ssl_channel_credentials()
        channel = grpc.secure_channel(
            f"{HOST}:{PORT}",
            channel_credentials,
        )

    client = ArmadaClient(channel)

    cancel_jobset(client)


if __name__ == "__main__":
    # Note that the form of ARMADA_SERVER should be something like
    # domain.com, localhost, or 0.0.0.0
    DISABLE_SSL = os.environ.get("DISABLE_SSL", False)
    HOST = os.environ.get("ARMADA_SERVER", "localhost")
    PORT = os.environ.get("ARMADA_PORT", "50051")

    cancel()
    print("Completed Workflow")

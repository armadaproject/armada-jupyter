"""
A more fledged out version of `simple.py` where we create a queue only
if it doesn't exist, and then create a jobset and job, and wait until
the job succeeds or fails.
"""

import os

import grpc
from armada_client import client as armada_client


def workflow():
    """
    Starts a workflow, which includes:
        - Creating a queue
        - Creating a jobset
        - Creating a job
    """

    # The queue and job_set_id that will be used for all jobs
    queue = "default"

    # Ensures that the correct channel type is generated
    if DISABLE_SSL:
        channel = grpc.insecure_channel(f"{HOST}:{PORT}")
    else:
        channel_credentials = grpc.ssl_channel_credentials()
        channel = grpc.secure_channel(
            f"{HOST}:{PORT}",
            channel_credentials,
        )

    client = armada_client.ArmadaClient(channel)

    queue_req = client.create_queue_request(name=queue, priority_factor=1)

    try:
        client.create_queue(queue_req)

    # Handle the error we expect to maybe occur
    except grpc.RpcError as e:
        code = e.code()
        if code == grpc.StatusCode.ALREADY_EXISTS:

            print(f"Queue {queue} already exists")
            queue_req = client.create_queue_request(name=queue, priority_factor=1)
            client.update_queue(queue_req)

        else:
            raise e


if __name__ == "__main__":
    # Note that the form of ARMADA_SERVER should be something like
    # domain.com, localhost, or 0.0.0.0
    DISABLE_SSL = os.environ.get("DISABLE_SSL", False)
    HOST = os.environ.get("ARMADA_SERVER", "localhost")
    PORT = os.environ.get("ARMADA_PORT", "50051")

    workflow()
    print("Completed Workflow")

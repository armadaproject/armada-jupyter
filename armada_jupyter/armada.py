"""
Example of getting jupyter notebook running on a k8s cluster.
"""


import grpc
from armada_client.client import ArmadaClient
from armada_client.armada import submit_pb2

from armada_jupyter.constants import HOST, PORT, DISABLE_SSL, JOB_SET_ID


def create_jupyter_service():
    """
    Create a jupyter service.
    """

    return submit_pb2.ServiceConfig(
        ports=[8888],
        type=submit_pb2.ServiceType.NodePort,
    )


def create_jupyter_ingress():
    """
    Create a jupyter ingress.
    """

    return submit_pb2.IngressConfig(ports=[8888], tls_enabled=False, use_clusterIP=True)


def create_armada_request(submission, client):
    priority = submission.armada_priority

    # Create the PodSpec for the job
    return client.create_job_request_item(
        priority=priority,
        pod_spec=submission.to_podspec(),
        ingress=[create_jupyter_ingress()],
        services=[create_jupyter_service()],
        labels={"app": "jupyter"},
    )


def submit(submission):
    """
    Starts a workflow for jupyter notebook.
    """

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

    queue = submission.armada_queue

    # Create the PodSpec for the job
    job_request_item = create_armada_request(submission, client)
    resp = client.submit_jobs(
        queue=queue, job_set_id=JOB_SET_ID, job_request_items=[job_request_item]
    )
    return resp, client

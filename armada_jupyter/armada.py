"""
Example of getting jupyter notebook running on a k8s cluster.
"""

import grpc
from armada_client.client import ArmadaClient

from armada_jupyter.constants import HOST, PORT, DISABLE_SSL

from armada_jupyter.submissions import Submission, Job


def create_armada_request(job: Job, client: ArmadaClient):

    # Create the PodSpec for the job
    return client.create_job_request_item(
        priority=job.priority,
        pod_spec=job.podspec,
        namespace=job.namespace,
        ingress=job.ingress,
        services=job.services,
        labels=job.labels,
        annotations=job.annotations,
    )


def submit(submission: Submission):
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

    queue = submission.queue
    job_set_id = submission.job_set_id

    # Create the PodSpec for the job
    job_request_items = [create_armada_request(job, client) for job in submission.jobs]
    resp = client.submit_jobs(
        queue=queue, job_set_id=job_set_id, job_request_items=job_request_items
    )
    return resp, client, len(job_request_items)

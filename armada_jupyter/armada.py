"""
Example of getting jupyter notebook running on a k8s cluster.
"""

import os

from armada_client.armada import submit_pb2
from armada_client.client import ArmadaClient
from armada_client.typings import EventType

from armada_jupyter.constants import TERMINAL_EVENTS
from armada_jupyter.submissions import Job, Submission


def create_armada_request(
    job: Job, client: ArmadaClient
) -> submit_pb2.JobSubmitRequestItem:

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


def submit(submission: Submission, job: Job, client: ArmadaClient) -> str:
    """
    Starts a workflow for jupyter notebook.
    """

    queue = submission.queue
    job_set_id = submission.job_set_id

    # Create the PodSpec for the job
    job_request_items = [create_armada_request(job, client)]
    resp = client.submit_jobs(
        queue=queue, job_set_id=job_set_id, job_request_items=job_request_items
    )

    job_id = resp.job_response_items[0].job_id
    return job_id


def construct_url(job: Job, job_id: str) -> str:
    """
    Constructs the URL for the Jupyter Notebook.

    The layout of this URL is defined here:
    https://github.com/G-Research/armada/blob/master/internal/
    executor/util/kubernetes_object.go#L95
    """

    domain = os.environ.get("ARMADA_DOMAIN", "domain.com")
    serviceport = job.podspec.containers[0].ports[0].containerPort
    container_name = job.podspec.containers[0].name
    namespace = job.namespace

    return (
        f"http://{container_name}-{serviceport}-"
        f"armada-{job_id}-0.{namespace}.{domain}"
    )


def check_job_status(client: ArmadaClient, submission: Submission, job_id: str) -> bool:
    """
    Uses the event stream to check the status of the job.

    Returns True if the job is running.
    """

    # complete an events loop
    event_stream = client.get_job_events_stream(
        queue=submission.queue, job_set_id=submission.job_set_id
    )

    # Checks that job Started correct
    for event in event_stream:

        event = client.unmarshal_event_response(event)

        # find the job_id that matches the event
        if event.message.job_id == job_id:

            if event.type == EventType.running:
                return True

            elif event.type in TERMINAL_EVENTS:
                return False

    return False

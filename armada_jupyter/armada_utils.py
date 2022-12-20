"""
Example of getting jupyter notebook running on a k8s cluster.
"""

import os
import re
import time

import grpc
from armada_client.armada import submit_pb2
from armada_client.client import ArmadaClient
from armada_client.event import Event
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
    Submits a workflow for jupyter notebooks.
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
    container = job.podspec.containers[0]
    serviceport = job.services[0].ports[0]
    namespace = job.namespace

    return (
        f"http://{container.name}-{serviceport}-"
        f"armada-{job_id}-0.{namespace}.{domain}"
    )


def check_job_status(client: ArmadaClient, submission: Submission, job_id: str) -> bool:
    """
    Uses the event stream to check the status of the job.

    Returns True if the job is running.
    """

    # There should never be a need for more than 3 tries,
    # as the job-set should be created relatively quickly.
    tries = 3

    while True:

        if tries == 0:
            raise Exception("Failed to start job - could not find event stream")

        try:
            # complete an events loop
            event_stream = client.get_job_events_stream(
                queue=submission.queue, job_set_id=submission.job_set_id
            )

            # Checks that job Started correct
            for event_wrapped in event_stream:

                event: Event = client.unmarshal_event_response(
                    event_wrapped
                )  # type: ignore

                # find the job_id that matches the event
                if event.message.job_id == job_id:

                    # If queued or pending
                    # Note: In theory this could just be pending, but incase that event
                    # is missed, we also check for queued.
                    if (
                        event.type == EventType.queued
                        or event.type == EventType.pending
                    ):
                        print("Job is Queued")
                        if not submission.wait_for_jobs_running:
                            return True

                    if event.type == EventType.running:
                        return True

                    elif event.type in TERMINAL_EVENTS:
                        return False

            # except grpc error
        except grpc.RpcError as e:

            # only error if details are not found
            if "testing for queue default" in e.details():

                tries -= 1
                time.sleep(1)

                continue

            else:
                print(e.details())
                raise e

    return False


def cancel_job(url: str, client: ArmadaClient) -> str:
    """
    Cancels the job associated with the URL.
    """

    # regex to find anything between armada- and -0
    result = re.search(r"armada-(.+?)-0", url)

    if result is None:
        raise Exception("Could not find job_id in URL")

    job_id = result.group(1)

    client.cancel_jobs(job_id=job_id)

    return job_id

"""
File to store default objects for testing
"""

from unittest.mock import Mock

import grpc
import pytest
from armada_client.armada.submit_pb2 import IngressConfig, ServiceConfig, ServiceType
from armada_client.client import ArmadaClient
from armada_client.k8s.io.api.core.v1 import generated_pb2 as core_v1
from armada_client.k8s.io.apimachinery.pkg.api.resource import (
    generated_pb2 as api_resource,
)
from armada_client.typings import EventType

from armada_jupyter.submissions import Job, Submission

JOB_ID = "testingID"

FAKE_PODSPEC_FULL = core_v1.PodSpec(
    containers=[
        core_v1.Container(
            name="jupyterlab",
            image="jupyter/tensorflow-notebook:latest",
            securityContext=core_v1.SecurityContext(runAsUser=1000),
            resources=core_v1.ResourceRequirements(
                requests={
                    "cpu": api_resource.Quantity(string="1"),
                    "memory": api_resource.Quantity(string="1Gi"),
                    "nvidia.com/gpu": api_resource.Quantity(string="1"),
                },
                limits={
                    "cpu": api_resource.Quantity(string="1"),
                    "memory": api_resource.Quantity(string="1Gi"),
                    "nvidia.com/gpu": api_resource.Quantity(string="1"),
                },
            ),
        )
    ],
)

FAKE_INGRESS = IngressConfig(ports=[8888], tls_enabled=False)

FAKE_SERVICE = ServiceConfig(type=ServiceType.NodePort, ports=[8888])

FAKE_JOB_GENERAL = Job(
    podspec=FAKE_PODSPEC_FULL,
    priority=1,
    namespace="jupyter",
    ingress=[FAKE_INGRESS],
    services=[FAKE_SERVICE],
    labels={"test": "test"},
    annotations={"test.com/annotation": "true"},
)


FAKE_SUBMISSION_GENERAL = Submission(
    queue="default",
    job_set_id="job-set-1",
    wait_for_jobs_running=True,
    jobs=[
        FAKE_JOB_GENERAL,
    ],
)


class FakeArmadaClient(ArmadaClient):
    def __init__(self, channel):
        self.channel = channel
        super().__init__(channel)

    def submit_jobs(self, *_, **__):

        resp = Mock()
        resp.job_response_items = [Mock()]
        resp.job_response_items[0].job_id = JOB_ID
        return resp

    def get_job_events_stream(self, *_, **__):
        """
        Yield a mock event for each call
        """

        yield Mock()

    @staticmethod
    def unmarshal_event_response(event):
        """
        In this case, we can just return the mock
        """
        event.message.job_id = JOB_ID
        event.type = EventType.running
        return event

    def cancel_jobs(self, job_id, *_, **__):
        # remove dashes from job_id since this is
        # outside of the scope of this class

        job_id = job_id.replace("-", "")
        assert job_id == JOB_ID


@pytest.fixture(scope="module")
def fake_armada_client():
    """
    Return a fake armada client
    """
    channel = grpc.insecure_channel("")
    return FakeArmadaClient(channel)


@pytest.fixture(scope="module")
def fake_podspec_full():
    """
    Return a fake podspec
    """
    return FAKE_PODSPEC_FULL


@pytest.fixture(scope="module")
def fake_ingress():
    """
    Return a fake ingress
    """
    return FAKE_INGRESS


@pytest.fixture(scope="module")
def fake_service():
    """
    Return a fake service
    """
    return FAKE_SERVICE


@pytest.fixture(scope="module")
def fake_submission_general():
    """
    Return a fake submission
    """
    return FAKE_SUBMISSION_GENERAL


@pytest.fixture(scope="module")
def fake_job_general():
    """
    Return a fake job
    """
    return FAKE_JOB_GENERAL


@pytest.fixture(scope="module")
def job_id_standard():
    """
    Return a fake job id
    """
    return JOB_ID

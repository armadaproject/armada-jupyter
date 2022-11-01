"""
Testing of the Armada utils functions
"""

import os
from concurrent import futures
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
from armada_jupyter.armada_utils import (
    check_job_status,
    construct_url,
    create_armada_request,
)
from armada_jupyter.submissions import Job, Submission

JOB_ID = "test_job_id"

os.environ["ARMADA_DOMAIN"] = "domain.com"

fake_podspec_full = core_v1.PodSpec(
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
            ports=[core_v1.ContainerPort(containerPort=8888)],
        )
    ],
)

fake_ingress = IngressConfig(ports=[8888], tls_enabled=False)

fake_service = ServiceConfig(type=ServiceType.NodePort, ports=[8888])

fake_job_general = Job(
    podspec=fake_podspec_full,
    priority=1,
    namespace="jupyter",
    ingress=[fake_ingress],
    services=[fake_service],
    labels={"test": "test"},
    annotations={"test.com/annotation": "true"},
)


fake_submission_general = Submission(
    queue="default",
    job_set_id="job-set-1",
    wait_for_jobs_running=True,
    jobs=[fake_job_general],
)


class FakeArmadaClient(ArmadaClient):
    def __init__(self, fake_channel):
        self.channel = fake_channel
        super().__init__(fake_channel)

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
        event.type = EventType.failed
        return event


@pytest.fixture(scope="session")
def server_mock():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    server.add_insecure_port("[::]:12345")
    server.start()

    yield
    server.stop(False)


channel = grpc.insecure_channel(target="127.0.0.1:12345")
tester = ArmadaClient(
    grpc.insecure_channel(
        target="127.0.0.1:12345",
        options={
            "grpc.keepalive_time_ms": 30000,
        }.items(),
    )
)


@pytest.mark.parametrize(
    "fake_sub, job_id",
    [(fake_submission_general, JOB_ID)],
)
def test_check_job_status(fake_sub, job_id):
    channel = grpc.insecure_channel("")

    job_successful = check_job_status(FakeArmadaClient(channel), fake_sub, job_id)

    assert job_successful is False


@pytest.mark.parametrize(
    "fake_job, job_id",
    [(fake_job_general, JOB_ID)],
)
def test_construct_url(fake_job, job_id):

    url = construct_url(fake_job, job_id)
    assert url == "http://jupyterlab-8888-armada-test_job_id-0.jupyter.domain.com"


@pytest.mark.usefixtures("server_mock")
@pytest.mark.parametrize(
    "fake_job",
    [fake_job_general],
)
def test_create_armada_request(fake_job):
    request = create_armada_request(fake_job, tester)
    assert request.pod_spec == fake_job.podspec
    assert request.ingress[0] == fake_job.ingress[0]
    assert request.services[0] == fake_job.services[0]
    assert request.priority == fake_job.priority
    assert request.namespace == fake_job.namespace
    assert request.labels == fake_job.labels
    assert request.annotations == fake_job.annotations

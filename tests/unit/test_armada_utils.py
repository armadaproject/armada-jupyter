"""
Testing of the Job and Submission utils functions
"""

import os
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
from armada_jupyter.armada import check_job_status, construct_url
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
    jobs=[fake_job_general],
)


class FakeArmadaClient(ArmadaClient):
    def __init__(self, channel):
        self.channel = channel
        super().__init__(channel)

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

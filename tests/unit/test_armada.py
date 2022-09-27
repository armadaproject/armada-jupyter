from concurrent import futures

import grpc
import pytest

from armada_client.armada.submit_pb2 import IngressConfig, ServiceConfig, ServiceType
from armada_client.client import ArmadaClient
from armada_client.k8s.io.api.core.v1 import generated_pb2 as core_v1
from armada_client.k8s.io.apimachinery.pkg.api.resource import (
    generated_pb2 as api_resource,
)
from armada_jupyter.armada import create_armada_request
from armada_jupyter.submissions import Job


@pytest.fixture(scope="session", autouse=True)
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


fake_ingress = IngressConfig(ports=[8888], tls_enabled=False)

fake_service = ServiceConfig(type=ServiceType.NodePort, ports=[8888])

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
        )
    ],
)

fake_job_general = Job(
    podspec=fake_podspec_full,
    priority=1,
    namespace="adam",
    ingress=[fake_ingress],
    services=[fake_service],
    labels={"test": "test"},
    annotations={"test.com/annotation": "true"},
)


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

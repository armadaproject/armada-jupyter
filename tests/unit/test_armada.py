import grpc
import pytest
from armada_client.armada import submit_pb2
from armada_client.client import ArmadaClient
from armada_client.k8s.io.api.core.v1 import generated_pb2 as core_v1
from armada_jupyter.armada import (
    create_armada_request,
    create_jupyter_ingress,
    create_jupyter_service,
)
from armada_jupyter.submissions import Submission

channel = grpc.insecure_channel("test")
client = ArmadaClient(channel)

ingress = submit_pb2.IngressConfig(ports=[8888], tls_enabled=False, use_clusterIP=True)

service = submit_pb2.ServiceConfig(
    ports=[8888],
    type=submit_pb2.ServiceType.NodePort,
)

labels = {"app": "jupyter"}


fake_submission_small = Submission(
    name="JupyterLab",
    image="jupyter/tensorflow-notebook:latest",
    armada_queue="default",
    armada_priority=1,
    timeout="36h",
)

fake_podspec_small = core_v1.PodSpec(
    containers=[
        core_v1.Container(
            name="JupyterLab",
            image="jupyter/tensorflow-notebook:latest",
            securityContext=core_v1.SecurityContext(runAsUser=1000),
            resources={},
        )
    ],
)


@pytest.mark.parametrize(
    "submission, podspec",
    [
        (fake_submission_small, fake_podspec_small),
    ],
)
def test_create_armada_request(submission, podspec):
    request = create_armada_request(submission, client)
    assert (
        request.priority == submission.armada_priority
    ), f"{request.priority} != {submission.armada_priority}"
    assert request.pod_spec == podspec, f"{request.pod_spec} \n\n {podspec} \n\n"
    assert request.ingress[0] == ingress, f"{request.ingress[0]} \n\n {ingress} \n\n"
    assert request.services[0] == service, f"{request.services[0]} \n\n {service} \n\n"
    assert request.labels == labels, f"{request.labels} \n\n {labels} \n\n"


@pytest.mark.parametrize(
    "func, expected",
    [
        (create_jupyter_ingress, ingress),
        (create_jupyter_service, service),
    ],
)
def test_k8s_object_creation(func, expected):
    assert func() == expected

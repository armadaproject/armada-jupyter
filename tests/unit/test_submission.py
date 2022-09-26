import pytest

from armada_client.armada.submit_pb2 import IngressConfig, ServiceConfig, ServiceType
from armada_client.k8s.io.api.core.v1 import generated_pb2 as core_v1
from armada_client.k8s.io.apimachinery.pkg.api.resource import (
    generated_pb2 as api_resource,
)
from armada_jupyter.submissions import Job, Submission, convert_to_submission

fake_podspec_full = core_v1.PodSpec(
    containers=[
        core_v1.Container(
            name="JupyterLab",
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

fake_ingress = IngressConfig(ports=[8888], tls_enabled=False)

fake_service = ServiceConfig(type=ServiceType.NodePort, ports=[8888])


fake_submission_general = Submission(
    queue="default",
    job_set_id="job-set-1",
    timeout="100s",
    jobs=[
        Job(
            podspec=fake_podspec_full,
            priority=1,
            namespace="adam",
            ingress=[fake_ingress],
            services=[fake_service],
        )
    ],
)


@pytest.mark.parametrize(
    "file,fake_submission",
    [
        (
            "tests/files/general.yml",
            fake_submission_general,
        )
    ],
)
def test_submission_creation(file, fake_submission):
    submission = convert_to_submission(file)

    assert submission.queue == fake_submission.queue
    assert submission.job_set_id == fake_submission.job_set_id
    assert submission.timeout == fake_submission.timeout
    assert (
        submission.jobs[0].podspec.containers[0].name
        == fake_submission.jobs[0].podspec.containers[0].name
    )
    assert (
        submission.jobs[0].podspec.containers[0].image
        == fake_submission.jobs[0].podspec.containers[0].image
    )
    assert (
        submission.jobs[0].podspec.containers[0].securityContext.runAsUser
        == fake_submission.jobs[0].podspec.containers[0].securityContext.runAsUser
    )
    assert (
        submission.jobs[0].podspec.containers[0].resources.requests["cpu"].string
        == fake_submission.jobs[0]
        .podspec.containers[0]
        .resources.requests["cpu"]
        .string
    )
    assert (
        submission.jobs[0].podspec.containers[0].resources.requests["memory"].string
        == fake_submission.jobs[0]
        .podspec.containers[0]
        .resources.requests["memory"]
        .string
    )
    assert (
        submission.jobs[0]
        .podspec.containers[0]
        .resources.requests["nvidia.com/gpu"]
        .string
        == fake_submission.jobs[0]
        .podspec.containers[0]
        .resources.requests["nvidia.com/gpu"]
        .string
    )
    assert (
        submission.jobs[0].podspec.containers[0].resources.limits["cpu"].string
        == fake_submission.jobs[0].podspec.containers[0].resources.limits["cpu"].string
    )
    assert (
        submission.jobs[0].podspec.containers[0].resources.limits["memory"].string
        == fake_submission.jobs[0]
        .podspec.containers[0]
        .resources.limits["memory"]
        .string
    )
    assert (
        submission.jobs[0]
        .podspec.containers[0]
        .resources.limits["nvidia.com/gpu"]
        .string
        == fake_submission.jobs[0]
        .podspec.containers[0]
        .resources.limits["nvidia.com/gpu"]
        .string
    )
    assert submission.jobs[0].priority == fake_submission.jobs[0].priority
    assert submission.jobs[0].namespace == fake_submission.jobs[0].namespace

    assert (
        submission.jobs[0].ingress[0].ports[0]
        == fake_submission.jobs[0].ingress[0].ports[0]
    )
    assert (
        submission.jobs[0].ingress[0].tls_enabled
        == fake_submission.jobs[0].ingress[0].tls_enabled
    )

    assert (
        submission.jobs[0].services[0].type == fake_submission.jobs[0].services[0].type
    )
    assert (
        submission.jobs[0].services[0].ports[0]
        == fake_submission.jobs[0].services[0].ports[0]
    )

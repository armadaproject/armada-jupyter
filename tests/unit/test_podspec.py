import pytest
import yaml

from armada_client.k8s.io.api.core.v1 import generated_pb2 as core_v1
from armada_client.k8s.io.apimachinery.pkg.api.resource import (
    generated_pb2 as api_resource,
)
from armada_jupyter.submissions import get_podspec

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


@pytest.mark.parametrize(
    "file,fake_podspec",
    [
        (
            "tests/files/general.yml",
            fake_podspec_full,
        )
    ],
)
def test_get_podspec(file, fake_podspec):
    with open(file, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    podspec = get_podspec(data)

    assert podspec.containers[0].name == fake_podspec.containers[0].name
    assert podspec.containers[0].image == fake_podspec.containers[0].image
    assert (
        podspec.containers[0].securityContext.runAsUser
        == fake_podspec.containers[0].securityContext.runAsUser
    )
    assert (
        str(podspec.containers[0].resources.requests["cpu"])
        == fake_podspec.containers[0].resources.requests["cpu"].string
    )
    assert (
        str(podspec.containers[0].resources.requests["memory"])
        == fake_podspec.containers[0].resources.requests["memory"].string
    )
    assert (
        str(podspec.containers[0].resources.requests["nvidia.com/gpu"])
        == fake_podspec.containers[0].resources.requests["nvidia.com/gpu"].string
    )
    assert (
        str(podspec.containers[0].resources.limits["cpu"])
        == fake_podspec.containers[0].resources.limits["cpu"].string
    )
    assert (
        str(podspec.containers[0].resources.limits["memory"])
        == fake_podspec.containers[0].resources.limits["memory"].string
    )
    assert (
        str(podspec.containers[0].resources.limits["nvidia.com/gpu"])
        == fake_podspec.containers[0].resources.limits["nvidia.com/gpu"].string
    )

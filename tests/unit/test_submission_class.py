"""
Testing Config class
"""

import pytest

from armada_client.k8s.io.api.core.v1 import generated_pb2 as core_v1
from armada_client.k8s.io.apimachinery.pkg.api.resource import (
    generated_pb2 as api_resource,
)

from armada_jupyter.submissions import (
    get_submissions,
    Submission,
    K8sResources,
    K8sResourceOptions,
)


fake_submission_full = Submission(
    name="JupyterLab",
    image="jupyter/tensorflow-notebook:latest",
    armada_queue="default",
    armada_priority=1,
    timeout="36h",
    resources=K8sResources(
        limits=K8sResourceOptions(cpu=1, memory="1Gi", nvidia_gpu=1),
        requests=K8sResourceOptions(cpu=1, memory="1Gi", nvidia_gpu=1),
    ),
)

fake_submission_no_req = Submission(
    name="JupyterLab",
    image="jupyter/tensorflow-notebook:latest",
    armada_queue="default",
    armada_priority=1,
    timeout="36h",
)

fake_submission_small_req = Submission(
    name="JupyterLab",
    image="jupyter/tensorflow-notebook:latest",
    armada_queue="default",
    armada_priority=1,
    timeout="36h",
    resources=K8sResources(
        limits=K8sResourceOptions(cpu=1, memory="1Gi"),
        requests=K8sResourceOptions(cpu=1, memory="1Gi"),
    ),
)

fake_submission_small = Submission(
    name="JupyterLab",
    image="jupyter/tensorflow-notebook:latest",
    armada_queue="default",
    armada_priority=1,
    timeout="1h",
)


@pytest.mark.parametrize(
    "file, fake_submission",
    [
        ("tests/files/test_sub_full.yml", fake_submission_full),
        ("tests/files/test_sub_no_req.yml", fake_submission_no_req),
        ("tests/files/test_sub_small_req.yml", fake_submission_small_req),
        ("tests/files/test_sub_small.yml", fake_submission_small),
    ],
)
def test_submission_gen(file, fake_submission):
    """
    Test get_config function
    """

    configs = get_submissions(file)
    assert str(configs[0]) == str(
        fake_submission
    ), f"{configs[0]} \n\n {fake_submission} \n\n"

    assert configs[0].timeout == fake_submission.timeout


@pytest.mark.parametrize(
    "file, real_timeout",
    [
        ("tests/files/test_sub_full.yml", "129600s"),
        ("tests/files/test_sub_no_req.yml", "129600s"),
        ("tests/files/test_sub_small_req.yml", "129600s"),
        ("tests/files/test_sub_small.yml", "3600s"),
    ],
)
def test_submission_timeout(file, real_timeout):
    """
    Test get_config function
    """

    configs = get_submissions(file)
    assert configs[0].timeout == real_timeout


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

fake_podspec_small = core_v1.PodSpec(
    containers=[
        core_v1.Container(
            name="JupyterLab",
            image="jupyter/tensorflow-notebook:latest",
            securityContext=core_v1.SecurityContext(runAsUser=1000),
            resources=core_v1.ResourceRequirements(
                requests={
                    "cpu": api_resource.Quantity(string="1"),
                    "memory": api_resource.Quantity(string="1Gi"),
                },
                limits={
                    "cpu": api_resource.Quantity(string="1"),
                    "memory": api_resource.Quantity(string="1Gi"),
                },
            ),
        )
    ],
)


@pytest.mark.parametrize(
    "file, fake_podspec",
    [
        ("tests/files/test_sub_full.yml", fake_podspec_full),
        ("tests/files/test_sub_small_req.yml", fake_podspec_small),
    ],
)
def test_podspec_conversion(file, fake_podspec):
    """
    Test if PodSpec was created correcty
    """

    configs = get_submissions(file)
    test_podspec = configs[0].to_podspec()

    assert str(test_podspec) == str(
        fake_podspec
    ), f"{test_podspec} \n\n {fake_podspec} \n\n"

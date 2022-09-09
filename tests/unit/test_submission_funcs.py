import pytest

from armada_jupyter.submissions import (
    K8sResources,
    K8sResourceOptions,
    k8s_resources_from_dict,
)


@pytest.mark.parametrize(
    "limits, requests, expected",
    [
        (
            {"cpu": 1, "memory": "1Gi", "nvidia.com/gpu": 1, "amd.com/gpu": 2},
            {"cpu": 1, "memory": "1Gi", "nvidia.com/gpu": 1, "amd.com/gpu": 2},
            K8sResources(
                limits=K8sResourceOptions(cpu=1, memory="1Gi", nvidia_gpu=1, amd_gpu=2),
                requests=K8sResourceOptions(
                    cpu=1, memory="1Gi", nvidia_gpu=1, amd_gpu=2
                ),
            ),
        ),
        (
            {"cpu": 1, "memory": "1Gi"},
            {"cpu": 1, "memory": "1Gi"},
            K8sResources(
                limits=K8sResourceOptions(cpu=1, memory="1Gi"),
                requests=K8sResourceOptions(cpu=1, memory="1Gi"),
            ),
        ),
    ],
)
def test_k8s_resources_from_dict(limits, requests, expected):
    """
    Test k8s_resources_from_dict function
    """

    resources = k8s_resources_from_dict(limits, requests)
    assert str(resources) == str(expected), f"{resources} \n\n {expected} \n\n"

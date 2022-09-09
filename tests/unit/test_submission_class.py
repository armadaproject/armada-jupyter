"""
Testing Config class
"""

import pytest

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
        limits=K8sResourceOptions(cpu=1, memory="1Gi", nvidia_gpu=1, amd_gpu=2),
        requests=K8sResourceOptions(cpu=1, memory="1Gi", nvidia_gpu=1, amd_gpu=2),
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

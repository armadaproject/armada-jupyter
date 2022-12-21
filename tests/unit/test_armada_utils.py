"""
Testing of the Armada utils functions
"""

import os

import grpc
import pytest
from armada_client.client import ArmadaClient
from armada_jupyter.armada_utils import (
    check_job_status,
    construct_url,
    create_armada_request,
)

os.environ["ARMADA_DOMAIN"] = "domain.com"

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
    [("fake_submission_general", "job_id_standard")],
)
def test_check_job_status(fake_sub, job_id, fake_armada_client, request):

    fake_sub = request.getfixturevalue(fake_sub)
    job_id = request.getfixturevalue(job_id)

    job_successful = check_job_status(fake_armada_client, fake_sub, job_id)

    assert job_successful is True


@pytest.mark.parametrize(
    "fake_job, job_id",
    [("fake_job_general", "job_id_standard")],
)
def test_construct_url(fake_job, job_id, job_id_standard, request):

    fake_job = request.getfixturevalue(fake_job)
    job_id = request.getfixturevalue(job_id)

    url = construct_url(fake_job, job_id)
    assert (
        url == f"http://jupyterlab-8888-armada-{job_id_standard}-0.jupyter.domain.com"
    )


@pytest.mark.usefixtures("server_mock")
@pytest.mark.parametrize(
    "fake_job",
    ["fake_job_general"],
)
def test_create_armada_request(fake_job, request):

    fake_job = request.getfixturevalue(fake_job)

    request = create_armada_request(fake_job, tester)
    assert request.pod_spec == fake_job.podspec
    assert request.ingress[0] == fake_job.ingress[0]
    assert request.services[0] == fake_job.services[0]
    assert request.priority == fake_job.priority
    assert request.namespace == fake_job.namespace
    assert request.labels == fake_job.labels
    assert request.annotations == fake_job.annotations

"""
Testing the submit function in __main__.py
"""

import os

import grpc
import pytest
from armada_client.client import ArmadaClient
from armada_jupyter.armada_utils import cancel_job


JOB_ID = "testingID"
TEST_URL = f"jupyterlab-8888-armada-{JOB_ID}-0.jupyter.domain"


# set variables in environment
os.environ["ARMADA_HOST"] = ""
os.environ["ARMADA_PORT"] = ""
os.environ["DISABLE_SSL"] = "True"


class FakeArmadaClient(ArmadaClient):
    def __init__(self, channel):
        self.channel = channel
        super().__init__(channel)

    def cancel_jobs(self, job_id, *_, **__):
        assert job_id == JOB_ID


@pytest.mark.parametrize(
    "fake_client, test_url",
    [(FakeArmadaClient, TEST_URL)],
)
def test_submit(fake_client, test_url):
    """
    Test the submit function
    """

    channel = grpc.insecure_channel("")
    fake_client = fake_client(channel)

    job_id = cancel_job(test_url, fake_client)
    assert job_id == JOB_ID

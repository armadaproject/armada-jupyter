"""
Testing the submit function in __main__.py
"""

import os
from unittest.mock import Mock

import grpc
import pytest
from armada_client.client import ArmadaClient
from armada_jupyter.armada_utils import cancel_job


JOB_ID = "testingID"
TEST_URL = f"jupyterlab-8888-armada-{JOB_ID}-0.jupyter.domain"

JOB_ID_WITH_DASH = "testing-ID"
TEST_URL_WITH_DASH = f"jupyterlab-8888-armada-{JOB_ID_WITH_DASH}-0.jupyter.domain"

TEST_URL_FAIL = "jupyter.domain.com"


# set variables in environment
os.environ["ARMADA_HOST"] = ""
os.environ["ARMADA_PORT"] = ""
os.environ["DISABLE_SSL"] = "True"


class FakeArmadaClient(ArmadaClient):
    def __init__(self, channel):
        self.channel = channel
        super().__init__(channel)

    def cancel_jobs(self, job_id, *_, **__):
        # remove dashes from job_id since this is
        # outside of the scope of this class

        job_id = job_id.replace("-", "")
        assert job_id == JOB_ID

        resp = Mock()
        resp.cancelled_ids = ["test"]

        return resp


@pytest.mark.parametrize(
    "fake_client, test_url, test_jobid, should_fail,",
    [
        (FakeArmadaClient, TEST_URL, JOB_ID, False),
        (FakeArmadaClient, TEST_URL_FAIL, None, True),
        (FakeArmadaClient, TEST_URL_WITH_DASH, JOB_ID_WITH_DASH, False),
    ],
)
def test_submit(fake_client, test_url, test_jobid, should_fail):
    """
    Test the submit function
    """

    channel = grpc.insecure_channel("")
    fake_client = fake_client(channel)

    if should_fail:
        with pytest.raises(Exception):
            job_id = cancel_job(test_url, fake_client)
        return

    job_id = cancel_job(test_url, fake_client)
    assert job_id == test_jobid

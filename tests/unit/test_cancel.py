"""
Testing the submit function in __main__.py
"""

import os

import pytest
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


@pytest.mark.parametrize(
    "test_url, test_jobid, should_fail,",
    [
        (TEST_URL, JOB_ID, False),
        (TEST_URL_FAIL, None, True),
        (TEST_URL_WITH_DASH, JOB_ID_WITH_DASH, False),
    ],
)
def test_submit(test_url, test_jobid, should_fail, fake_armada_client):
    """
    Test the submit function
    """

    if should_fail:
        with pytest.raises(Exception):
            job_id = cancel_job(test_url, fake_armada_client)
        return

    job_id = cancel_job(test_url, fake_armada_client)
    assert job_id == test_jobid

"""
Testing the submit function in __main__.py
"""

import os
from unittest.mock import Mock

import grpc
import pytest
from armada_client.client import ArmadaClient
from armada_client.typings import EventType
from armada_jupyter.__main__ import app, submit_worker
from typer.testing import CliRunner

runner = CliRunner()

TEST_FILE = "tests/files/general.yml"
JOB_ID = "test_job_id"

# set variables in environment
os.environ["ARMADA_HOST"] = ""
os.environ["ARMADA_PORT"] = ""
os.environ["DISABLE_SSL"] = "True"


class FakeArmadaClient(ArmadaClient):
    def __init__(self, channel):
        self.channel = channel
        super().__init__(channel)

    def submit_jobs(self, *_, **__):

        resp = Mock()
        resp.job_response_items = [Mock()]
        resp.job_response_items[0].job_id = JOB_ID
        return resp

    def get_job_events_stream(self, *_, **__):
        """
        Yield a mock event for each call
        """

        yield Mock()

    @staticmethod
    def unmarshal_event_response(event):
        """
        In this case, we can just return the mock
        """
        event.message.job_id = JOB_ID
        event.type = EventType.running
        return event


@pytest.mark.parametrize(
    "fake_client, test_file",
    [(FakeArmadaClient, TEST_FILE)],
)
def test_submit(fake_client, test_file, capsys):
    """
    Test the submit function
    """

    channel = grpc.insecure_channel("")

    fake_client = fake_client(channel)

    submit_worker(test_file, fake_client)

    captured = capsys.readouterr()
    assert (
        "Getting Submission Objects from tests/files/general.yml" in captured.out
    ), captured.out
    assert "Submitting 1 Jobs to Armada" in captured.out, captured.out
    assert (
        "http://jupyterlab-8888-armada-test_job_id-0.jupyter.domain.com" in captured.out
    ), captured.out


def test_app():
    file = "Not File"
    result = runner.invoke(app, [file])

    # This fails as the file cannot be found
    # We will make this test more complicated in future,
    # But for now it should be fine
    assert result.exit_code == 1, result.stdout
    assert "Getting Submission Objects" in result.stdout, result.stdout
    assert file in result.stdout, result.stdout

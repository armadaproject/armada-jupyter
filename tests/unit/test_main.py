"""
Testing the submit function in __main__.py
"""

import os

import pytest
from typer.testing import CliRunner

from armada_jupyter.__main__ import app, submit_worker

runner = CliRunner()

TEST_FILE = "tests/files/general.yml"
JOB_ID = "test_job_id"

# set variables in environment
os.environ["ARMADA_HOST"] = ""
os.environ["ARMADA_PORT"] = ""
os.environ["DISABLE_SSL"] = "True"


@pytest.mark.parametrize(
    "test_file",
    [(TEST_FILE)],
)
def test_submit(test_file, fake_armada_client, job_id_standard, capsys):
    """
    Test the submit function
    """

    submit_worker(test_file, fake_armada_client)

    captured = capsys.readouterr()
    assert (
        "Getting Submission Objects from tests/files/general.yml" in captured.out
    ), captured.out
    assert "Submitting 1 Jobs to Armada" in captured.out, captured.out
    assert (
        f"http://jupyterlab-8888-armada-{job_id_standard}-0.jupyter.domain.com"
        in captured.out
    ), captured.out


def test_app():
    file = "Not File"
    result = runner.invoke(app, ["submit", file])

    # This fails as the file cannot be found
    # We will make this test more complicated in future,
    # But for now it should be fine
    assert result.exit_code == 1, result.stdout
    assert "Getting Submission Objects" in result.stdout, result.stdout
    assert file in result.stdout, result.stdout

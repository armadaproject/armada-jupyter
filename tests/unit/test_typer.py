"""
Testing for typer
"""

from typer.testing import CliRunner

from armada_jupyter.__main__ import app

runner = CliRunner()

JOB_ID = "test_job_id"


def test_submit():
    file = "Not File"
    result = runner.invoke(app, ["submit", file])

    # This fails as the file cannot be found
    # We will make this test more complicated in future,
    # But for now it should be fine
    assert result.exit_code == 1, result.stdout
    assert "Getting Submission Objects" in result.stdout, result.stdout
    assert file in result.stdout, result.stdout


def test_cancel():
    url = f"jupyterlab-8888-armada-{JOB_ID}-0.jupyter.domain"
    result = runner.invoke(app, ["cancel", url])

    assert result.exit_code == 1, result.stdout

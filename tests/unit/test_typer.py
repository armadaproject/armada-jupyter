"""
Testing for typer
"""

from typer.testing import CliRunner

from armada_jupyter.__main__ import app

runner = CliRunner()


def test_app():
    file = "Not File"
    result = runner.invoke(app, [file])

    # This fails as the file cannot be found
    # We will make this test more complicated in future,
    # But for now it should be fine
    assert result.exit_code == 1, result.stdout
    assert "Getting Submission Objects" in result.stdout, result.stdout
    assert file in result.stdout, result.stdout

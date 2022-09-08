"""
Testing for typer
"""

from typer.testing import CliRunner

from armada_jupyter.__main__ import app

runner = CliRunner()


def test_app():
    file = "test.yaml"
    result = runner.invoke(app, [file])

    assert result.exit_code == 0, result.stdout
    assert "Submitting pods from" in result.stdout, result.stdout
    assert file in result.stdout, result.stdout

"""
Testing for typer
"""

from typer.testing import CliRunner

from armada_jupyter.__main__ import app

runner = CliRunner()


def test_app():
    result = runner.invoke(app, ["submit", "test.yaml"])
    assert result.exit_code == 0
    assert "Hello Camila" in result.stdout
    assert "Let's have a coffee in Berlin" in result.stdout

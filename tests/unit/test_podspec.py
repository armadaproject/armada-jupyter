import pytest
import yaml

from armada_jupyter.podspec import create_podspec_object


@pytest.mark.parametrize(
    "file,fake_podspec",
    [
        (
            "tests/files/general.yml",
            "fake_podspec_full",
        )
    ],
)
def test_get_podspec(file, fake_podspec, request):
    with open(file, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    fake_podspec = request.getfixturevalue(fake_podspec)

    podspec = create_podspec_object(data["jobs"][0]["podSpec"])

    assert podspec.containers[0].name == fake_podspec.containers[0].name
    assert podspec.containers[0].image == fake_podspec.containers[0].image
    assert (
        podspec.containers[0].securityContext.runAsUser
        == fake_podspec.containers[0].securityContext.runAsUser
    )
    assert (
        podspec.containers[0].resources.requests["cpu"].string
        == fake_podspec.containers[0].resources.requests["cpu"].string
    )
    assert (
        podspec.containers[0].resources.requests["memory"].string
        == fake_podspec.containers[0].resources.requests["memory"].string
    )
    assert (
        podspec.containers[0].resources.requests["nvidia.com/gpu"].string
        == fake_podspec.containers[0].resources.requests["nvidia.com/gpu"].string
    )
    assert (
        podspec.containers[0].resources.limits["cpu"].string
        == fake_podspec.containers[0].resources.limits["cpu"].string
    )
    assert (
        podspec.containers[0].resources.limits["memory"].string
        == fake_podspec.containers[0].resources.limits["memory"].string
    )
    assert (
        podspec.containers[0].resources.limits["nvidia.com/gpu"].string
        == fake_podspec.containers[0].resources.limits["nvidia.com/gpu"].string
    )

import pytest

from armada_jupyter.submissions import convert_to_submission


@pytest.mark.parametrize(
    "file,fake_submission",
    [
        (
            "tests/files/general.yml",
            "fake_submission_general",
        )
    ],
)
def test_submission_creation(file, fake_submission, request):
    submission = convert_to_submission(file)

    fake_submission = request.getfixturevalue(fake_submission)

    assert submission.queue == fake_submission.queue
    assert submission.job_set_id == fake_submission.job_set_id
    assert (
        submission.jobs[0].podspec.containers[0].name
        == fake_submission.jobs[0].podspec.containers[0].name
    )
    assert (
        submission.jobs[0].podspec.containers[0].image
        == fake_submission.jobs[0].podspec.containers[0].image
    )
    assert (
        submission.jobs[0].podspec.containers[0].securityContext.runAsUser
        == fake_submission.jobs[0].podspec.containers[0].securityContext.runAsUser
    )
    assert (
        submission.jobs[0].podspec.containers[0].resources.requests["cpu"].string
        == fake_submission.jobs[0]
        .podspec.containers[0]
        .resources.requests["cpu"]
        .string
    )
    assert (
        submission.jobs[0].podspec.containers[0].resources.requests["memory"].string
        == fake_submission.jobs[0]
        .podspec.containers[0]
        .resources.requests["memory"]
        .string
    )
    assert (
        submission.jobs[0]
        .podspec.containers[0]
        .resources.requests["nvidia.com/gpu"]
        .string
        == fake_submission.jobs[0]
        .podspec.containers[0]
        .resources.requests["nvidia.com/gpu"]
        .string
    )
    assert (
        submission.jobs[0].podspec.containers[0].resources.limits["cpu"].string
        == fake_submission.jobs[0].podspec.containers[0].resources.limits["cpu"].string
    )
    assert (
        submission.jobs[0].podspec.containers[0].resources.limits["memory"].string
        == fake_submission.jobs[0]
        .podspec.containers[0]
        .resources.limits["memory"]
        .string
    )
    assert (
        submission.jobs[0]
        .podspec.containers[0]
        .resources.limits["nvidia.com/gpu"]
        .string
        == fake_submission.jobs[0]
        .podspec.containers[0]
        .resources.limits["nvidia.com/gpu"]
        .string
    )
    assert submission.jobs[0].priority == fake_submission.jobs[0].priority
    assert submission.jobs[0].namespace == fake_submission.jobs[0].namespace

    assert (
        submission.jobs[0].ingress[0].ports[0]
        == fake_submission.jobs[0].ingress[0].ports[0]
    )
    assert (
        submission.jobs[0].ingress[0].tls_enabled
        == fake_submission.jobs[0].ingress[0].tls_enabled
    )

    assert (
        submission.jobs[0].services[0].type == fake_submission.jobs[0].services[0].type
    )
    assert (
        submission.jobs[0].services[0].ports[0]
        == fake_submission.jobs[0].services[0].ports[0]
    )
    assert submission.wait_for_jobs_running == fake_submission.wait_for_jobs_running

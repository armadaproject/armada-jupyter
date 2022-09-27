import os


class YMLSTR:
    """
    This class is used to store the yml strings for the different
    services that are used in the armada-jupyter config.
    """

    JOBS = "jobs"

    PODSPEC = "podSpec"
    PRIORITY = "priority"
    NAMESPACE = "namespace"
    INGRESS = "ingress"
    SERVICES = "services"
    LABELS = "labels"
    ANNOTATIONS = "annotations"

    QUEUE = "queue"
    JOB_SET_ID = "jobSetId"
    TIMEOUT = "timeout"


DISABLE_SSL = os.environ.get("DISABLE_SSL", False)
HOST = os.environ.get("ARMADA_SERVER", "localhost")
PORT = os.environ.get("ARMADA_PORT", "50051")

JOB_SET_ID = "armada-jupyter-pods"

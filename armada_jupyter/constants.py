class YMLSTR:
    """
    This class is used to store the yml strings for the different
    services that are used in the armada-jupyter config.
    """

    submissions = "submissions"

    name = "name"
    image = "image"
    armada_queue = "armada_queue"
    armada_priority = "armada_priority"
    timeout = "timeout"
    resources = "resources"

    limits = "limits"
    requests = "requests"
    cpu = "cpu"
    memory = "memory"
    nvidia_gpu = "nvidia.com/gpu"
    amd_gpu = "amd.com/gpu"


DEFAULT_QUEUE = "default"
DEFAULT_PRIORITY = 1
DEFAULT_TIMEOUT = "1h"

DEFAULT_MEMORY = "1Gi"
DEFAULT_CPU = 1

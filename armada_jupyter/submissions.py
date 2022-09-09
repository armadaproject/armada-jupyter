from typing import List, Optional, Dict, Union

import yaml

from armada_jupyter.constants import (
    YMLSTR,
    DEFAULT_QUEUE,
    DEFAULT_PRIORITY,
    DEFAULT_TIMEOUT,
    DEFAULT_MEMORY,
    DEFAULT_CPU,
)


class K8sResourceOptions:
    """
    Manages the options for a kubernetes resource request or limit
    """

    def __init__(
        self,
        cpu: int,
        memory: str,
        nvidia_gpu: Union[str, int, None] = None,
        amd_gpu: Union[str, int, None] = None,
    ):
        self.cpu = cpu
        self.memory = memory
        self.nvidia_gpu = nvidia_gpu
        self.amd_gpu = amd_gpu

        # If they exist, they might be a string, so we need to convert them to int
        if self.nvidia_gpu:
            self.nvidia_gpu = int(self.nvidia_gpu)

        if self.amd_gpu:
            self.amd_gpu = int(self.amd_gpu)

    def __repr__(self) -> str:
        return (
            f"K8sResourceOptions({YMLSTR.cpu}={self.cpu}, {YMLSTR.memory}='{self.memory}', "
            f"{YMLSTR.nvidia_gpu}={self.nvidia_gpu}, {YMLSTR.amd_gpu}={self.amd_gpu})"
        )


class K8sResources:
    """
    Manages the resources for a Kubernetes pod ran by Armada
    """

    def __init__(
        self, limits: K8sResourceOptions = None, requests: K8sResourceOptions = None
    ):
        if limits is None and requests is None:
            raise ValueError("Must specify at least one of limits or requests")

        self.limits = limits
        self.requests = limits

    def __repr__(self) -> str:
        return f"K8sResources({YMLSTR.limits}={self.limits}, {YMLSTR.requests}={self.requests})"


class Submission:
    """
    Represents a Armada-Jupyter Submission
    """

    def __init__(
        self,
        name: str,
        image: str,
        armada_queue: str,
        armada_priority: int,
        timeout: str,
        resources: Optional[K8sResources] = None,
    ):
        self.name = name
        self.image = image
        self.armada_queue = armada_queue
        self.armada_priority = armada_priority
        self.timeout = self.timeout_conversion(timeout)
        self.resources = resources

        # Check that resources is the right object
        if not isinstance(resources, K8sResources) and resources is not None:
            raise ValueError(
                f"resources must be a K8sResources object, not {type(resources)}"
            )

    @staticmethod
    def timeout_conversion(timeout: str) -> Optional[str]:
        """
        Convert timeout from minutes and hours into seconds.

        timeout can be in the form of 10m or 5h for example

        should return a string like 100s
        """

        if timeout[-1] == "m":
            return str(int(timeout[:-1]) * 60) + "s"
        elif timeout[-1] == "h":
            return str(int(timeout[:-1]) * 60 * 60) + "s"
        elif timeout[-1] == "s":
            return timeout

        ValueError("Timeout must be in the form of [x]h, [x]m or [x]s")
        return None

    def resources_from_dict(
        self, resources: Dict[str, Dict[str, Union[str, int]]]
    ) -> None:
        """
        Used for adding a resources from dict
        """

        self.resources = k8s_resources_from_dict(
            limits=resources.get(YMLSTR.limits),
            requests=resources.get(YMLSTR.requests),
        )

    def __repr__(self) -> str:
        return (
            f"Submission(f{YMLSTR.name}='{self.name}', {YMLSTR.image}='{self.image}' "
            f"{YMLSTR.armada_queue}='{self.armada_queue}', "
            f"{YMLSTR.armada_priority}={self.armada_priority}, "
            f"{YMLSTR.timeout}='{self.timeout}', {YMLSTR.resources}={self.resources})"
        )


def k8s_resources_from_dict(
    limits: Optional[Dict[str, Union[str, int]]] = None,
    requests: Optional[Dict[str, Union[str, int]]] = None,
) -> K8sResources:
    """
    Creates a K8sResources object from a dict
    """

    changed: Dict[str, Optional[K8sResourceOptions]] = {}

    if limits is None and requests is None:
        raise ValueError("Must specify at least one of limits or requests")

    # Use a loop to save repeated code.
    for key, needs_changed in [(YMLSTR.limits, limits), (YMLSTR.requests, requests)]:
        if needs_changed is None:
            changed[key] = None
            continue

        # We use .get() here because we don't want to raise an error if the key
        # doesn't exist.
        changed[key] = K8sResourceOptions(
            cpu=int(needs_changed.get(YMLSTR.cpu, DEFAULT_CPU)),
            memory=str(needs_changed.get(YMLSTR.memory, DEFAULT_MEMORY)),
            nvidia_gpu=needs_changed.get(YMLSTR.nvidia_gpu, None),
            amd_gpu=needs_changed.get(YMLSTR.amd_gpu, None),
        )

    return K8sResources(
        limits=changed[YMLSTR.limits],
        requests=changed[YMLSTR.requests],
    )


def get_submissions(file) -> List[Submission]:
    """
    Creates the submissions from a YAML file
    """

    submissions = []

    with open(file, "r", encoding="utf-8") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)

        for submission in config[YMLSTR.submissions]:

            # pop out resources key
            resources = submission.pop(YMLSTR.resources, None)

            # check for missing mandatory keys
            for key in [YMLSTR.name, YMLSTR.image]:
                if key not in submission:
                    raise ValueError(f"Missing mandatory key {key}")

            # create submission object
            # We use .get() for the optional keys so that we don't raise an error
            submission = Submission(
                name=submission[YMLSTR.name],
                image=submission[YMLSTR.image],
                armada_queue=submission.get(YMLSTR.armada_queue, DEFAULT_QUEUE),
                armada_priority=submission.get(
                    YMLSTR.armada_priority, DEFAULT_PRIORITY
                ),
                timeout=submission.get(YMLSTR.timeout, DEFAULT_TIMEOUT),
            )

            # Insert resources seperately. This is because we need want to
            # support both a dict and a K8sResources object.
            if resources:
                submission.resources_from_dict(resources)

            submissions.append(submission)

    return submissions

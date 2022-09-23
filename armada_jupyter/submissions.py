from typing import List, Optional

import yaml
from armada_client.armada.submit_pb2 import IngressConfig, ServiceConfig


class Job:
    def __init__(
        self,
        podspec,
        priority: int = None,
        namespace: str = None,
        ingress: List[IngressConfig] = None,
        services: List[ServiceConfig] = None,
    ):
        self.podspec = podspec
        self.priority = priority
        self.namespace = namespace
        self.ingress = ingress
        self.services = services

    def __repr__(self) -> str:
        return (
            f"Jobs({self.podspec}, {self.priority}, {self.namespace}, "
            f"{self.ingress}, {self.services})"
        )


class Submission:
    """
    Represents a Armada-Jupyter Submission
    """

    def __init__(self, queue: str, job_set_id: str, timeout: str, jobs: List[Job]):
        self.queue = queue
        self.job_set_id = job_set_id
        self.timeout = self.timeout_conversion(timeout)
        self.jobs = jobs

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

        raise ValueError("Timeout must be in the form of [x]h, [x]m or [x]s")

    def __repr__(self) -> str:
        return (
            f"Submission(queue={self.queue}, job_set_id={self.job_set_id}, "
            f"timeout={self.timeout}, jobs={self.jobs})"
        )


def convert_to_object(file: str) -> Submission:
    """
    Converts a yaml file into a Submission object
    """

    with open(file, "r", encoding="utf-8") as stream:
        data = yaml.safe_load(stream)

    jobs = []

    for job in data["jobs"]:
        podspec = job.get("podSpec")
        priority = job.get("priority")
        namespace = job.get("namespace")
        ingress = job.get("ingress")
        services = job.get("services")

        podspec = get_podspec(data)

        ingress_configs = []

        if ingress is not None:
            for i in ingress:
                ingress_configs.append(
                    IngressConfig(
                        type=i.get("type"),
                        ports=i.get("ports"),
                        annotations=i.get("annotations"),
                        tls_enabled=i.get("tlsEnabled"),
                        cert_name=i.get("certName"),
                        use_clusterIP=i.get("useClusterIP"),
                    )
                )

        service_configs = []

        if services is not None:
            for s in services:
                service_configs.append(
                    ServiceConfig(
                        type=s.get("type"),
                        ports=s.get("ports"),
                    )
                )

        jobs.append(Job(podspec, priority, namespace, ingress_configs, service_configs))

    return Submission(data["queue"], data["jobSetId"], data["timeout"], jobs)

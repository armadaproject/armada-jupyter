"""
Example of getting jupyter notebook running on a k8s cluster.
"""

import os

import grpc
from armada_client.client import ArmadaClient
from armada_client.k8s.io.api.core.v1 import generated_pb2 as core_v1
from armada_client.k8s.io.apimachinery.pkg.api.resource import (
    generated_pb2 as api_resource,
)
from armada_client.armada import submit_pb2


def create_jupyter_pod():
    """
    Create a jupyter pod with a single container.
    """

    return core_v1.PodSpec(
        hostNetwork=True,
        setHostnameAsFQDN=True,
        containers=[
            core_v1.Container(
                name="jupyter-notebook",
                image="jupyter/tensorflow-notebook:latest",
                ports=[core_v1.ContainerPort(containerPort=8888)],
                securityContext=core_v1.SecurityContext(runAsUser=1000),
                resources=core_v1.ResourceRequirements(
                    requests={
                        "cpu": api_resource.Quantity(string="2000m"),
                        "memory": api_resource.Quantity(string="2000Mi"),
                    },
                    limits={
                        "cpu": api_resource.Quantity(string="2000m"),
                        "memory": api_resource.Quantity(string="2000Mi"),
                    },
                ),
            )
        ],
    )


def create_jupyter_service():
    """
    Create a jupyter service.
    """

    return submit_pb2.ServiceConfig(
        ports=[8888],
        type=submit_pb2.ServiceType.NodePort,
    )


def create_jupyter_ingress():
    """
    Create a jupyter ingress.
    """

    return submit_pb2.IngressConfig(ports=[8888], tls_enabled=False)


def jupyter_workflow():
    """
    Starts a workflow for jupyter notebook.
    """

    # The queue and job_set_id that will be used for all jobs
    queue = "jupyter-queue"
    job_set_id = "jupyter-jobset"

    # Ensures that the correct channel type is generated
    if DISABLE_SSL:
        channel = grpc.insecure_channel(f"{HOST}:{PORT}")
    else:
        channel_credentials = grpc.ssl_channel_credentials()
        channel = grpc.secure_channel(
            f"{HOST}:{PORT}",
            channel_credentials,
        )

    client = ArmadaClient(channel)

    queue_req = client.create_queue_request(name=queue, priority_factor=1)
    # Make sure we handle the queue already existing
    try:
        client.create_queue(queue_req)

    # Handle the error we expect to maybe occur
    except grpc.RpcError as e:
        code = e.code()
        if code == grpc.StatusCode.ALREADY_EXISTS:
            print(f"Queue {queue} already exists")

        else:
            raise e

    # Create the PodSpec for the job
    job_request_item = client.create_job_request_item(
        priority=1,
        pod_spec=create_jupyter_pod(),
        ingress=[create_jupyter_ingress()],
        services=[create_jupyter_service()],
        labels={"app": "jupyter"},
    )
    client.submit_jobs(
        queue=queue, job_set_id=job_set_id, job_request_items=[job_request_item]
    )


if __name__ == "__main__":
    # Note that the form of ARMADA_SERVER should be something like
    # domain.com, localhost, or 0.0.0.0
    DISABLE_SSL = os.environ.get("DISABLE_SSL", False)
    HOST = os.environ.get("ARMADA_SERVER", "localhost")
    PORT = os.environ.get("ARMADA_PORT", "50051")

    jupyter_workflow()
    print("Completed Workflow")

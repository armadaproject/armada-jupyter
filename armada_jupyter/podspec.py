from armada_client.k8s.io.api.core.v1 import generated_pb2 as core_v1
from armada_client.k8s.io.apimachinery.pkg.api.resource import (
    generated_pb2 as api_resource,
)


PodSpec = core_v1.PodSpec
Containers = core_v1.Container
SecurityContext = core_v1.SecurityContext
ResourceRequirements = core_v1.ResourceRequirements
Quantity = api_resource.Quantity


def create_podspec_object(podspec_dict: dict) -> core_v1.PodSpec:
    """
    Creates a PodSpec object from a dictionary.

    Ensures that the correct types are used for the PodSpec object.
    """

    for container in podspec_dict["containers"]:
        if "resources" in container:

            if "limits" in container["resources"]:
                container["resources"]["limits"] = {
                    key: Quantity(string=str(value))
                    for key, value in container["resources"]["limits"].items()
                }

            if "requests" in container["resources"]:
                container["resources"]["requests"] = {
                    key: Quantity(string=str(value))
                    for key, value in container["resources"]["requests"].items()
                }

    # check that length of containers is exactly 1
    # if not, raise an error
    if len(podspec_dict["containers"]) != 1:
        raise ValueError(
            "Only one container per pod is supported. Please check your podspec."
        )

    # serviceport = job.podspec.containers[0].ports[0].containerPort
    # container_name = job.podspec.containers[0].name
    # namespace = job.namespace
    # check these values are present in the podspec
    # if not, raise an error

    if "containers" not in podspec_dict:
        raise ValueError("Please specify a container in your podspec.")

    if "ports" not in podspec_dict["containers"][0]:
        raise ValueError("Please specify a port in your podspec.")

    if "containerPort" not in podspec_dict["containers"][0]["ports"][0]:
        raise ValueError("Please specify a containerPort in your podspec.")

    if "name" not in podspec_dict["containers"][0]:
        raise ValueError("Please specify a name for the containers in your podspec.")

    return core_v1.PodSpec(**podspec_dict)

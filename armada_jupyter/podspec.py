from armada_client.k8s.io.api.core.v1 import generated_pb2 as core_v1
from armada_client.k8s.io.apimachinery.pkg.api.resource import (
    generated_pb2 as api_resource,
)


PodSpec = core_v1.PodSpec
Containers = core_v1.Container
SecurityContext = core_v1.SecurityContext
ResourceRequirements = core_v1.ResourceRequirements
Quantity = api_resource.Quantity


def create_podspec_object(podspec_dict):
    # serach whole dict for a key "resources"
    # if found, create a new dict with the same key and value

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

    return core_v1.PodSpec(**podspec_dict)

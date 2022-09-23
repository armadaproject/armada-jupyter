from armada_client.k8s.io.api.core.v1 import generated_pb2 as core_v1

PodSpec = core_v1.PodSpec
Containers = core_v1.Container
SecurityContext = core_v1.SecurityContext
ResourceRequirements = core_v1.ResourceRequirements


def get_podspec(data: dict) -> PodSpec:
    # extract podSpec from data
    podSpec = data["jobs"][0]["podSpec"]

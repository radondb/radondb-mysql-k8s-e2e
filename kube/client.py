from kubernetes import client, config, utils

# Configs can be set in Configuration class directly or using helper utility
config.load_kube_config()

class ClientSingleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = client.CoreV1Api()
        return cls._instance
class CustomResourceClientSingleton:
    _instance = None
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = client.CustomObjectsApi()
        return cls._instance

def create(yaml_dict):
    pass
from typing import List
from kubernetes import client, config, utils
from kubernetes.stream import stream

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

def runSQL(namespace, podname, sql):
    return kubeExec(namespace, podname, 'mysql', ['mysql', '-uroot', '-e', sql])

def runSQLJustResult(namespace, podname, sql):
    return kubeExec(namespace, podname, 'mysql', ['mysql', '-uroot','-sN', '-e', sql])
def kubeExec(namespace, podname, containter, cmd):
    client = ClientSingleton()
    #for exmaple cmd= ['mysql', '-uroot', '-e', 'show slave status\\G']
    exec_command = stream(client.connect_get_namespaced_pod_exec, podname, namespace, command=cmd, container=containter,
                           stderr=True, stdin=False, stdout=True, tty=False)
    return exec_command

def findLeaderPod(namespace) -> str:
    client = ClientSingleton()
    pods = client.list_namespaced_pod(namespace)
    for pod in pods.items:
        if pod.metadata.labels.get('app.kubernetes.io/name') == 'mysql' and pod.metadata.labels.get('role') == 'LEADER':
            return pod.metadata.name
def findFollowerPod(namespace) -> List[str]:
    client = ClientSingleton()
    pods = client.list_namespaced_pod(namespace)
    follower_pods = []
    for pod in pods.items:
        if pod.metadata.labels.get('app.kubernetes.io/name') == 'mysql' and pod.metadata.labels.get('role') == 'FOLLOWER':
            follower_pods.append(pod.metadata.name)
    return follower_pods  
def findSeconds_Behind_Master(namespace, name)->int:
    client = ClientSingleton()
    exec_command = kubeExec(namespace, name, 'mysql', ['mysql', '-uroot', '-e', 'show slave status\\G'])
    for line in exec_command.splitlines():
        if 'Seconds_Behind_Master' in line:
            # 分割行以提取值
            key, value = line.split(':', 1)
            seconds_behind_master = value.strip()
            print(f"Found Seconds_Behind_Master: {seconds_behind_master}")
            return int(seconds_behind_master)
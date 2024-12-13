from kube import ClientSingleton
from typing import Tuple
from helm import CheckAndInstallHelm, InstallMysqlOperator, UninstallOperator
def checkManger() -> Tuple[str, str, bool]:
    c = ClientSingleton()
    try:
        ret = c.list_namespaced_pod(namespace='default')
        for i in ret.items:
            if i.metadata.name.startswith('demo-mysql'):
                    # check all container_statuses ready
                    if all(i.status.container_statuses[j].ready for j in range(len(i.status.container_statuses))):
                        return i.status.phase, "true", True
                    return i.status.phase, "false", True
    except Exception as e:
        print(e)
        return "", "", False
    
    return "","", False
def waitReady():
    while True:
        s, r, ok = checkManger()
        if ok:
            if r == "true":
                return
            else:
                print("waiting for mysql manager to be ready")
        else:
            print("waiting for helm to be ready")
def prepare():
    s,r, ok = checkManger()

    if not ok:
         CheckAndInstallHelm()
         InstallMysqlOperator()
    else:
        if r != "true":
            waitReady()


# check the helm command exist
import os
import subprocess
import sys, time
from kube import ClientSingleton
def CheckAndInstallHelm():
    try:
        subprocess.check_output(["helm", "version"])
        return True
    except Exception:
        subprocess.call(["bash", "-c", "curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash"])
        return False
def InstallMysqlOperator():
    try:
        subprocess.check_output(["helm", "repo", "add", "radondb", "https://radondb.github.io/radondb-mysql-kubernetes/"])
        subprocess.check_output(["helm", "install", "demo", "radondb/mysql-operator"])

        return True
    except Exception:
       return False
def UninstallOperator():
    try:
        subprocess.check_output(["helm", "uninstall", "demo"])
        return True
    except Exception:
        return False

if __name__ == '__main__':
    CheckAndInstallHelm()
    InstallMysqlOperator()
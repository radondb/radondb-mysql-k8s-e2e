# test rebuild
from k8stest.mysql import rebuildPod

def test_rebuild() -> bool:
    return rebuildPod("sample-mysql-1", "0")


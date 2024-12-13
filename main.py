from k8stest import prepare, final
from k8stest.mysql import changeReplica


if __name__ == '__main__':
    prepare()
    try:
        changeReplica(4)
    except Exception as e:
            print(e)


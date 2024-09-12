import pytest
from k8stest import prepare, final
from k8stest.mysql import changeReplica


class TestReplicas:
    def setup_module(self, module):
        print("setup module")
        prepare()
    def teardown_module(self, module):
        print("teardown module")
        final()
    def test_Replicas4(self):

        try:
            changeReplica(4)
        except Exception as e:
            assert e.status ==  422
            return
        assert False


    def test_Replicas0(self):

        try:
            changeReplica(0)
        except Exception as e:

            assert False
            return
        assert True
    
    def test_Replicas2(self):

        try:
            changeReplica(2)
        except Exception as e:
            assert False
            return
        assert True

    def test_Replicas3(module):
        prepare()
        try:
            changeReplica(3)
        except Exception as e:
            assert False
            return
        assert True


    def test_Replicas1(self):
        prepare()
        try:
            changeReplica(1)
        except Exception as e:
            assert False
            return
        assert True
    def test_Replicas5(self):
        prepare()
        try:
            changeReplica(5)
        except Exception as e:
            assert False
            return
        assert True



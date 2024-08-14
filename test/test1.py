from k8stest import prepare, final
from k8stest.mysql import changeReplica


class TestBase:
    def setup_module(module):
        prepare()


    def teardown_module(module):
        final()


class TestReplicas(TestBase):
    def test_Replicas4(module):

        try:
            changeReplica(4)
        except Exception as e:
            assert e.status ==  422
            return
        assert False


    def test_Replicas0(module):

        try:
            changeReplica(0)
        except Exception as e:

            assert False
            return
        assert True
    
    def test_Replicas2(module):

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

    def test_Replicas5(module):
        prepare()
        try:
            changeReplica(5)
        except Exception as e:
            assert False
            return
        assert True
    def test_Replicas1(module):
        prepare()
        try:
            changeReplica(1)
        except Exception as e:
            assert False
            return
        assert True



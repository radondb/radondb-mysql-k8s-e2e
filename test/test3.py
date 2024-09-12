import pytest
from kube.client import runSQL,runSQLJustResult, findFollowerPod, findLeaderPod, findSeconds_Behind_Master
sql = '''
create database test; use test;
create table test (id int primary key, name varchar(255));
insert into test values (1, 'test');
'''     
class TestReplication:
    def setup_method(self, method):
        """在每个测试方法执行之前运行"""
        print("\nSetup: Preparing resources for", method.__name__)

        self.leader = findLeaderPod("default")
        self.follower = findFollowerPod("default")
        
        exec_cmd = runSQL("default", self.leader, sql)
        print(exec_cmd)

    
    def teardown_method(self, method):
        """在每个测试方法执行之后运行"""
        print("\nTeardown: Cleaning up after", method.__name__)
        exec_cmd = runSQL("default", self.leader, "drop database test;")
        print(exec_cmd)
        self.resource = None

    def test_leaderExist(self):
        assert len(self.leader) != 0
        print("Running test_example1")

    def test_behindSecond(self):
        assert len(self.follower) != 0
        for f in self.follower:
            assert findSeconds_Behind_Master("default", f) == 0

    def test_followerExist(self):
        assert len(self.follower) != 0

    def test_databaseExist(self):
        assert runSQLJustResult("default", self.leader, "show databases like 'test';") == "test\n"
        assert runSQLJustResult("default", self.follower[0], "show databases like 'test';") == "test\n"
        assert runSQLJustResult("default", self.follower[1], "show databases like 'test';") == "test\n"
    
    def test_dataConsistent(self):
        assert runSQLJustResult("default", self.leader, "select * from test.test;") == "1\ttest\n"
        for f in self.follower:
            assert runSQLJustResult("default", f, "select * from test.test;") == "1\ttest\n"


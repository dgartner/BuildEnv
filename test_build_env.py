#!usr/bin/python
from build_env import EnvironmentBuilder
import unittest


class TestBuildEnv(object):
    def setUp(self):
        """Setup env before each test, gets called before each test"""
        version = "40"
        root = "D:\\wr_envs\\pytest"

        self._eb = EnvironmentBuilder(version, root)

        # Here you could write a fake zip file or something, in a different
        # path than the actual zipfile

    def tearDown(self):
        """Tear down env after each test, tests called after each test"""

        # Here, you could delete the fake zipfile you made in setup

    def test_unzip_products(self):
        self._eb._unzip_products()

    def test_mod_profile(self):
        self._eb._mod_profile()
        
    def test_run_profile(self):
        self._eb._run_profile()
        
    def test_run_setup(self):
        self._eb._run_setup()
    
    def test_build_bases(self):
        self._eb._build_bases()
        
    def test_build_and_run_setlicense(self):
        self._eb._build_and_run_setlicense()


if __name__ == "__main__":
    # Can't just run all unit tests, since there isn't a good way to automate verification
    tbe = TestBuildEnv()
    tbe.setUp()
    tbe.test_run_profile()
    tbe.test_run_setup()


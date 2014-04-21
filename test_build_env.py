from build_env import EnvironmentBuilder
import unittest


class TestBuildEnv(unittest.TestCase):
    def setUp(self):
        """Setup env before each test, gets called before each test"""
        version = "fake-version"
        work_request = "fake-work-request"
        root = "fake-root"

        self._eb = EnvironmentBuilder(version, work_request, root)

        # Here you could write a fake zip file or something, in a different
        # path than the actual zipfile

    def tearDown(self):
        """Tear down env after each test, tests called after each test"""

        # Here, you could delete the fake zipfile you made in setup

    def test_unzip_products(self):
        """Test unzip products method

        Call the method 'self._eb._unzip_products()' and verify it worked.
        """

    def test_mod_profile(self):
        """Test mod profile method

        Call the method 'self._eb._mod_profile()' and verify it worked.
        """


if __name__ == "__main__":
    unittest.main()

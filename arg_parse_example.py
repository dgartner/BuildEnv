import argparse
import zipfile
import os


class EnvironmentBuilder(object):
    def __init__(self, version, work_request, force, env_root):
        self._version = version
        self._work_request = work_request
        self._force = force
        self._env_root = env_root

    def _unzip_products(self):
        version = self._version
        wr = self._work_request
        env_root = self._env_root

        archive_path = os.path.join("D:", "archive", version)
        if wr is not None:
            env_path = os.path.join("D:", "wr_envs", wr, "monarch")
        else:
            env_path = os.path.abspath(env_root)

        for zip_name in os.listdir(archive_path):
            zip = zipfile.ZipFile(archive_path + zip_name)
            zip.extractall(env_path)

    def _setup_root_env(self):
        pass  # TODO: Implement me

    def start(self):
        """Start the party"""
        self._unzip_based_on_version()
        self._setup_root_env()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')

    # Setup required/positional arguments
    parser.add_argument("version", help="Version")  # not optional

    # Setup optional arguments
    parser.add_argument("-w", "--workrequest", help="Name or ID of Work Request")
    parser.add_argument("-r", "--root", help="Path to env root")
    parser.add_argument("-f", "--force", default=False, action="store_true", help="Force something")
    args = parser.parse_args()

    # get the arg values
    version = args.version
    env_root = args.root
    force = args.force
    work_request = args.workrequest

    # Setup our env builder
    env_builder = EnvironmentBuilder(version, work_request, force, env_root)

    # Kick it off
    env_builder.start()

    print "Complete."

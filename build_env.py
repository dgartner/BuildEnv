#!usr/bin/python
import os
import sys
import zipfile
import argparse

class EnvironmentBuilder(object):
    
    def __init__(self, version, wr, root):
        self._version = version
        self._wr = wr
        self._root = root
        self._osi = os.path.join(root, 'monarch')
        self._job = os.path.join(root, 'job')
        
    def _set_root(self, new_root):
        self._root = new_root
        self._osi = os.path.join(self._root, 'monarch')
        self._job = os.path.join(self._root, 'job')
        print "root: " + self._root
        print "osi: " + self._osi
        print "job: " + self._job
        
    def _unzip_products(self):
        archive_path = os.path.join('D:\\archive' + self._version)
        print "searching " + archive_path + " for zip files"
        
        if self._wr != None:
            self._set_root(os.path.join("D:\\wr_envs", self._wr))
            
        for zip_name in os.listdir(archive_path):
            zip_file = zipfile.ZipFile(os.path.join(archive_path, zip_name))
            zip_file.extractall(self._osi)
            print "unzipping " + zip_name + " to " + self._osi

    def _mod_profile(self):
        new_prof = open(os.path.join(self._osi, 'monarch_xp.bat'), 'w+')
        old_prof = open(os.path.join(self._osi, 'scripts', 'monarch_xp.bat'))
        for line in old_prof:
            if "SET OSIINET=" in line:
                new_prof.write("SET OSIINET=" + self._osi + "\n")
            elif "SET OSI=" in line:
                new_prof.write("SET OSI=" + self._osi + "\n")
            elif "SET JOB=" in line:
                new_prof.write("SET JOB=" + self._job + "\n")
            elif "SET OSIUSER=" in line:
                new_prof.write("SET OSIUSER=840\n")
            elif "SET OBJSOCK=" in line:
                new_prof.write("SET OBJSOCK=840\n")
            else:
                new_prof.write(line)

    def start(self):
        self._unzip_products()
        self._mod_profile()
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Build development environment')
    
    parser.add_argument("-v", "--version", default="44", help="Environment version to build")
    parser.add_argument("-w", "--wr", default=None, help="WR number")
    parser.add_argument("-r", "--root", default=os.path.join('D:\\osi'), help="Path to environment root")
    parser.add_argument("-c", "--clean", default=False, action="store_true", help="delete current environment if root is not empty")
    args = parser.parse_args()
    
    env_builder = EnvironmentBuilder(args.version, args.wr, args.root)
    
    env_builder.start()


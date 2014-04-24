#!usr/bin/python
import os
import zipfile
import argparse

class EnvironmentPreparer(object):
    def __init__(self, version, root):
        self._version = version
        self._root = root
        self._osi = os.path.join(root, 'monarch')
        self._job = os.path.join(root, 'osi_cust')
        self._log_dir = os.path.join(self._osi, "setup_logs")
        
    def _unzip_products(self):
        archive_path = os.path.join('D:\\archive' + self._version)
        print "searching " + archive_path + " for zip files"
            
        for zip_name in os.listdir(archive_path):
            zip_file = zipfile.ZipFile(os.path.join(archive_path, zip_name))
            zip_file.extractall(self._osi)
            print "unzipping " + zip_name + " to " + self._osi

    def _mod_profile(self):
        with open(os.path.join(self._osi, 'monarch_xp.bat'), 'w+') as new_prof, \
                open(os.path.join(self._osi, 'scripts', 'monarch_xp.bat')) as old_prof:
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
                elif "vcvars32 x86" in line:
                    if self._version=="40":
                        new_prof.write("call \"C:\\Program Files (x86)\\Microsoft Visual Studio 8\\VC\\vcvarsall.bat\"\n")
                    else:
                        new_prof.write(line)
                else:
                    new_prof.write(line)
                    
    def start(self):
        self._unzip_products()
        self._mod_profile()                  
                    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Build development environment')
    
    parser.add_argument("root", help="Path to environment root")
    
    parser.add_argument("-v", "--version", default="44", help="Environment version to build")
    parser.add_argument("-c", "--clean", default=False, action="store_true", help="delete current environment if root is not empty")
    args = parser.parse_args()
    
    env_prep = EnvironmentPreparer(args.version, args.root)
    
    env_prep.start()
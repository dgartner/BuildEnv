#!usr/bin/python
import os
import zipfile
import argparse
import subprocess

class EnvironmentBuilder(object):
    
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
                
    def _run_profile(self):
        with open(os.path.join(self._log_dir, "profile.log"), 'w+') as profile_log:
            print "Running monarch_xp.bat -- Saving output to " + profile_log
            p = subprocess.Popen("monarch_xp.bat DEBUG", shell=True, stdout=profile_log, stderr=profile_log)
            p.wait()
        
    def _run_setup(self):
        with open(os.path.join(self._log_dir, "setup.log"), 'w+') as setup_log:
            print "Running setup -- Saving output to " + setup_log
            p = subprocess.Popen("setup", shell=True, stdout=setup_log, stderr=setup_log)
            p.wait()
        
        with open(os.path.join(self._log_dir, "toolkit_setup.log"), 'w+') as tk_setup_log:
            print "Running toolkit_setup -- Saving output to " + tk_setup_log
            p = subprocess.Popen("toolkit_setup", shell=True, stdout=tk_setup_log, stderr=tk_setup_log)
            p.wait()
        
        p = subprocess.Popen("tkprofile", shell=True)
        p.wait()
        
    def _build_bases(self):
        with open(os.path.join(self._log_dir, "base_net.log"), 'w+') as base_net_log:
            print "Building base_net"
            os.chdir(os.path.join(self._osi, "src", "base_net"))
            p = subprocess.Popen("make", shell=True, stdout=base_net_log, stderr=base_net_log)
            p.wait()
        
        with open(os.path.join(self._log_dir, "base.log"), 'w+') as base_log:
            print "Building base"
            os.chdir(os.path.join(self._osi, "src", "base"))
            p = subprocess.Popen("make", shell=True, stdout=base_log, stderr=base_log)
            p.wait()
        
    def _build_and_run_setlicense(self):
        with open(os.path.join(self._log_dir, "setlicense.log"), 'w+') as setlicense_log:
            print "building setlicense"
            os.chdir(os.path.join(self._osi, "src", "base", "util", "license", "setlicense"))
            p = subprocess.Popen("make", shell=True, stdout=setlicense_log, stderr=setlicense_log)
            p.wait()
            
            p = subprocess.Popen("osi_setlicense -easy", shell=True, stdout=setlicense_log, stderr=setlicense_log)
            p.wait()        
    
    def start(self):
        self._unzip_products()
        self._mod_profile()
        self._run_profile()
        self._run_setup()
        self._build_bases()
        self._build_and_run_setlicense()
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Build development environment')
    
    parser.add_argument("root", help="Path to environment root")
    
    parser.add_argument("-v", "--version", default="44", help="Environment version to build")
    parser.add_argument("-c", "--clean", default=False, action="store_true", help="delete current environment if root is not empty")
    args = parser.parse_args()
    
    env_builder = EnvironmentBuilder(args.version, args.root)
    
    env_builder.start()


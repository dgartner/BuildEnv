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
        
    def _run_setup(self):
        log_name = os.path.join(self._log_dir, "profile.log")
        d = os.path.dirname(log_name)
        if not os.path.exists(d):
            os.makedirs(d)
            
        log_name = os.path.join(self._log_dir, "setup.log") 
        with open(log_name, 'w+') as log:
            print "Running setup -- Saving output to " + log_name
            p = subprocess.Popen("setup", shell=True, cwd=self._osi, stdout=log, stderr=log)
            p.wait()
        
        log_name = os.path.join(self._log_dir, "toolkit_setup.log")
        with open(log_name, 'w+') as log:
            print "Running toolkit_setup -- Saving output to " + log_name
            p = subprocess.Popen("toolkit_setup", shell=True, cwd=self._osi, stdout=log, stderr=log)
            p.wait()
        
    def _build_bases(self):
        with open(os.path.join(self._log_dir, "base_net.log"), 'w+') as log:
            print "Building base_net"
            p = subprocess.Popen("make", shell=True, cwd=os.path.join(self._osi, "src", "base_net"), stdout=log, stderr=log)
            p.wait()
        
        with open(os.path.join(self._log_dir, "base.log"), 'w+') as log:
            p = subprocess.Popen("make", shell=True, cwd=os.path.join(self._osi, "src", "base"), stdout=log, stderr=log)
            p.wait()
        
    def _build_and_run_setlicense(self):
        with open(os.path.join(self._log_dir, "setlicense.log"), 'w+') as log:
            print "building setlicense"
            os.chdir(os.path.join(self._osi, "src", "base", "util", "license", "setlicense"))
            p = subprocess.Popen("make", shell=True, cwd=self._osi, stdout=log, stderr=log)
            p.wait()
            
            p = subprocess.Popen("osi_setlicense -easy", shell=True, stdout=log, stderr=log)
            p.wait()
            
    def _build_src(self):
        with open(os.path.join(self._log_dir, "makesrc.log"), 'w+') as log:
            print "building src"
            p = subprocess.Popen("make", shell=True, cwd=os.path.join(self._osi, "src"), stdout=log, stderr=log)
            p.wait()
    
    def _build_srcNet(self):
        with open(os.path.join(self._log_dir, "makesrcNet.log"), 'w+') as log:
            print "building srcNET"
            p = subprocess.Popen("makecs", shell=True, cwd=os.path.join(self._osi, "srcNET"), stdout=log, stderr=log)
            p.wait()
            
    def _build_srcJava(self):
        with open(os.path.join(self._log_dir, "makesrcJava.log"), 'w+') as log:
            print "building srcJava"
            p = subprocess.Popen("make", shell=True, cwd=os.path.join(self._osi, "srcJava"), stdout=log, stderr=log)
            p.wait()
            
    def start(self):
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


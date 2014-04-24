#!usr/bin/python
import os
import argparse
import subprocess
import shutil

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
        with open(os.path.join(self._log_dir, "build_setlicense.log"), 'w+') as log:
            print "Building setlicense"
            p = subprocess.Popen("make", shell=True, cwd=os.path.join(self._osi, "src", "base", "util", "license", "setlicense"), stdout=log, stderr=log)
            p.wait()
            
        with open(os.path.join(self._log_dir, "osi_setlicense.log"), 'w+') as log:
            print "setting license"    
            p = subprocess.Popen("osi_setlicense -easy", shell=True, stdout=log, stderr=log)
            p.wait()
            
    def _run_schema_all(self):
        with open(os.path.join(self._log_dir, "schema_all.log"), 'w+') as log:
            print "running schema_all"
            p = subprocess.Popen("schema_all", shell=True, cwd=self._osi, stdout=log, stderr=log)
            p.wait()
            
    def _run_pop_base(self):
        with open(os.path.join(self._log_dir, "pop_base.log"), 'w+') as log:
            print "running pop_base"
            p = subprocess.Popen("pop_base", shell=True, cwd=self._osi, stdout=log, stderr=log)
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
            
    def _mod_security(self):
        old_path = os.path.join(self._osi, "sys", "rc", "security.rc")
        new_path = os.path.join(self._job, "sys", "rc", "security.rc") 
        print "Editing security.rc"
        with open(old_path, 'w+') as sec_old, \
                open(new_path, 'w+') as sec_new:
            for line in sec_old:
                line.replace('dac1b', 'DGARTNER')
                line.replace('dac2b', '')
                line.replace('dac1a', '')
                line.replace('dac2a', '')
                sec_new.write(line)
            
        os.remove(old_path)
        shutil.move(new_path, old_path)
        os.remove(new_path)
        
    def _uds_import(self):
        with open(os.path.join(self._log_dir, "uds_import.log"), 'w+') as log:
            print "running osii_uds_import"
            p = subprocess.Popen("osii_uds_import --domain SAMPLE --new", shell=True, cwd=self._osi, stdout=log, stderr=log)
            p.wait()
    
    def _settings_import(self):
        with open(os.path.join(self._log_dir, "settings_import.log"), 'w+') as log:
            print "running osii_settings_import"
            p = subprocess.Popen("osii_settings_import --domain SAMPLE --all", shell=True, cwd=self._osi, stdout=log, stderr=log)
            p.wait()
            
    def _states_converter(self):
        with open(os.path.join(self._log_dir, "states_converter.log"), 'w+') as log:
            print "running osii_states_converter"
            p = subprocess.Popen("osii_states_converter", shell=True, cwd=self._osi, stdout=log, stderr=log)
            p.wait()
            
    def _mod_CONFIG_SERV(self):
        old_path = os.path.join(self._osi, "data", "CONFIG_SERV.DAT")
        new_path = os.path.join(self._job, "data", "CONFIG_SERV.tmp")
        print "Editing CONFIG_SERV.DAT" 
        with open(old_path, 'w+') as config_old, \
                open(new_path, 'w+') as config_new:
            for line in config_old:
                line.replace('dac1b', 'DGARTNER')
                line.replace('dac2b', '')
                line.replace('dac1a', '')
                line.replace('dac2a', '')
                config_new.write(line)
        
        os.remove(old_path)
        shutil.move(new_path, old_path)
        os.remove(new_path)
        
        
            
    def start(self):
        self._run_setup()
        self._build_bases()
        self._build_and_run_setlicense()
        self._run_schema_all()
        self._run_pop_base()
        self._build_src()
        self._build_srcNet()
        self._build_srcJava()
        self._mod_security()
        self._uds_import()
        self._settings_import()
        self._states_converter()
        self._mod_CONFIG_SERV()
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Build development environment')
    
    parser.add_argument("root", help="Path to environment root")
    
    parser.add_argument("-v", "--version", default="44", help="Environment version to build")
    parser.add_argument("-c", "--clean", default=False, action="store_true", help="delete current environment if root is not empty")
    args = parser.parse_args()
    
    env_builder = EnvironmentBuilder(args.version, args.root)
    
    env_builder.start()


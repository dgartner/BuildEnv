#!usr/bin/python
import os
import sys
import zipfile

def unzip_products(version=44):
    if int(version) == 40:
        archive = "D:\\archive40\\"
        env = "D:\\osi40_test\\monarch"
    elif int(version) == 44:
        archive = "D:\\archive44\\"
        env = "D:\\osi44_test\\monarch"

    for zip_name in os.listdir(archive):
        zip = zipfile.ZipFile(archive + zip_name)
        zip.extractall(env)
            
if __name__ == "__main__":
    num_args = len(sys.argv)
    if num_args != 2:
        print ('Please specify version number')
        exit(0)
    else:
        version = int(sys.argv[1])
    unzip_products(version)


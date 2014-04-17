#!usr/bin/python
import os
import sys
import zipfile

num_args = len(sys.argv)

if num_args == 1:
    archive = "D:\\archive44\\"
elif num_args > 1:
    ver = sys.argv[1]
    if int(ver) == 40:
        archive = "D:\\archive40\\"
        env = "D:\\osi40_test\\monarch"
    elif int(ver) == 44:
        archive = "D:\\archive44\\"
        env = "D:\\osi44_test\\monarch"

for zip_name in os.listdir(archive):
    zip = zipfile.ZipFile(archive + zip_name)
    zip.extractall(env)
            


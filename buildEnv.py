#!usr/bin/python
import os
import sys
import zipfile
import getopt

def unzip_products(arg):
    archive_path = "D:\\archive" + arg['version'] + "\\"
    if arg['wr'] != None:
        env_path = "D:\\wr_envs\\" + arg['wr'] + "\\"
    else:
        env_path = arg['path']

    for zip_name in os.listdir(archive_path):
        zip = zipfile.ZipFile(archive_path + zip_name)
        zip.extractall(env_path)

def usage():
    print ("Your arguments are bad!")

def handle_arguments(arg):
    arg['version'] = "44"
    arg['path'] = "D:\\osi\\"
    arg['force'] = False
    arg['wr'] = None

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hfv:p:w:", 
                ["help", "version=", "path="])
    except getopt.GetoptError as err:
        print str(err)
        usage()
        sys.exit(2)

    for o, a in opts:
        if o in ('-v', '--version'):
            arg['version'] = a
        elif o in ('-p', '--path'):
            arg['path'] = a
        elif o == '-f':
            arg['force'] = True
        elif o == 'w':
            arg['wr'] = a
        else:
            assert False, "unhandled option"

if __name__ == "__main__":
    arg = {}
    handle_arguments(arg)
    unzip_products(arg)


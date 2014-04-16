#!usr/bin/python
import os
import listdir
import sys

numArgs = len(sys.argv)

if numArgs == 1:
    archive = "D:\\archive44"
else if numArgs > 1:
    ver = sys.argv[1]
    if int(ver) == 40:
        archive = "D:\\archive40"
    else if int(ver) == 44:
        archive = "D:\\archive44"

zips = os.listdir(archive)

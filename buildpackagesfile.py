#!/usr/bin/env python

import tarfile, zipfile, gzip
import glob
import re
import os
import shutil
import StringIO
from optparse import OptionParser

from os import listdir
from os.path import isfile, join
from itertools import imap

#
# Build PACKAGES file from tar.gz and zip R packages
#
path = "."
targzpart = ".tar.gz"
zippart = ".zip"
extensions = targzpart, zippart
packages_file = "PACKAGES"

def get_description_name(filename):
	namepart=re.search("(.*)_", filename).group(1)	
	return namepart + os.sep + "DESCRIPTION"	

# Read a file from a targz archive
def read_file_in_targz(filename):

	print "Processing gzip: " + filename + " \n"
	with tarfile.open(filename, "r:gz") as tar:		
		descfile = get_description_name(filename)
		content = tar.extractfile(descfile).read()		
		return content

# Read a file from a zip archive
def read_file_in_zip(filename):

	print "Processing zip: " + filename + " \n"	
	with zipfile.ZipFile(filename) as zfile:
		
		descfile = get_description_name(filename)
		doscontent = StringIO.StringIO(zfile.read(descfile)).getvalue()			
		# Convert dos line endings
		return re.sub("\r(?!\n)|(?<!\r)\n", "\r\n", doscontent)

# Append to the packages file
def append_to_packages(content):
	with open(packages_file, "a") as f:
		f.write(content + "\n")		

# Read the DESCRIPTION file from the archive
def add_description_from_file(filename):
	if targzpart in filename:
		content = read_file_in_targz(filename)	
		append_to_packages(content)
	if zippart in filename:
		content = read_file_in_zip(filename)
		append_to_packages(content)

# Check to see if this is an archive to be included
def is_archive(file):
	return any(imap(file.__contains__, extensions))

# Gzip the PACKAGES file
def gzip_packages_file():	
	with open(packages_file, "rb") as f:
		with gzip.open(packages_file + ".gz", "wb") as gzout:
			gzout.writelines(f)			

# Build all the packages
def build_all_packages():
	# Backup old package file (if it exists)
	if os.path.isfile(packages_file):
   		shutil.move(packages_file, packages_file + ".bk")	

	# Look for matching files in the current directory
	files = [ f for f in listdir(path) if isfile(join(path,f)) and is_archive(f) ]
	for f in files:
		add_description_from_file(f)

	gzip_packages_file()	
# Main method
if  __name__ =="__main__":

	parser = OptionParser()	
	parser.add_option("-b", action="store_true", dest="buildall", default=False, help="Build all packages")
	parser.add_option("-a", dest="packagename", help="Append a packagename to PACKAGES (e.g. ggplot2_0.9.3.1.tar.gz)")
	(options, args) = parser.parse_args()
	
	if options.buildall:
		build_all_packages
	elif options.packagename:		
		add_description_from_file(options.packagename)
	else:
		print parser.print_help()
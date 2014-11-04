#!/usr/bin/python

# A simple python implementation of external sorting.
# For small files (i.e. files that can fit into memory), sort the file with python's native list.sort() function.
# For big files, split the file into small ones and perform multi-pass merge sort.
# The result will be outputted to the standard output, which is the same behaviour with bash's "sort" utility function.
# I wrote this script in such a situation:
# * I needed to sort a big file (including non-ASCII characters) and process it with a python script. 
# * Firstly, I tried bash's sort utility program but found the output is different from the result python's sort().
# * Since I needed to process it later in python's order, so I came up with a python implementation of external sorting. 

import sys
import string
import math
import shutil
import os

# set memory limit for internal sorting: 1GB
MEM_LIMIT=1024*1024*1024

def sort_small_file(filename):
	fp = open(filename, "r")
	lines = fp.readlines()
	fp.close()
	lines.sort()
	fp_w = open(filename, "w")
	for line in lines:
		fp_w.write(line)
	fp_w.close()

def merge_two_sorted_files(file_a, file_b, file_merged):
	fp_a = open(file_a, "r")
	fp_b = open(file_b, "r")
	fp_w = open(file_merged, "w")
	line_a = fp_a.readline()
	line_b = fp_b.readline()
	while line_a and line_b:
		if line_a < line_b:
			fp_w.write(line_a)
			line_a = fp_a.readline()
		elif line_a > line_b:
			fp_w.write(line_b)
			line_b = fp_b.readline()
		else:
			fp_w.write(line_b)
			line_b = fp_b.readline()
	while line_a:
		fp_w.write(line_a)
		line_a = fp_a.readline()
	fp_a.close()
	while line_b:
		fp_w.write(line_b)
		line_b = fp_b.readline()
	fp_b.close()
	fp_w.close()

def split_big_file(bigfile, mem_limit, tmpdir):
	fp = open(bigfile, "r")
	chunk_id = 0
	fp_w = open(tmpdir+"/0_"+str(chunk_id), "w")
	chunk_size = 0
	line = fp.readline()
	while line:
		if chunk_size+len(line) <= mem_limit:
			fp_w.write(line)
			chunk_size += len(line)
		else:
			fp_w.close()
			chunk_id += 1
			fp_w = open(tmpdir+"/0_"+str(chunk_id), "w")
			fp_w.write(line)
			chunk_size = len(line)
		line = fp.readline()
	fp_w.close()
	fp.close()
	return chunk_id+1

def sort_big_file(bigfile, tmpdir):
	chunk_num = split_big_file(bigfile, MEM_LIMIT, tmpdir)
	# sort small files separately:
	for i in range(0, chunk_num):
		small_file_name = tmpdir +"/0_"+str(i)
		sort_small_file(small_file_name)
	# merge sorted files:
	pass_num = int(math.ceil(math.log(chunk_num, 2)))
	for j in range(0, pass_num): # pass id
		upper_index = int(min(math.pow(2,pass_num-j), chunk_num))
		for k in range(0, upper_index, 2): # seg id
			file_a = tmpdir +"/"+str(j)+"_"+str(k)
			file_merged = tmpdir+"/"+str(j+1)+"_"+str(k/2)
			if k == upper_index-1:
				shutil.copyfile(file_a, file_merged)
				os.remove(file_a)
			else:
				file_b = tmpdir +"/"+str(j)+"_"+str(k+1)
				merge_two_sorted_files(file_a, file_b, file_merged)
				os.remove(file_a)
				os.remove(file_b)
	final_file = tmpdir+"/"+str(pass_num)+"_0"
	fp = open(final_file, "r")
	line = fp.readline()
	while line:
		sys.stdout.write(line)
		line = fp.readline()
	fp.close()
	os.remove(final_file)
	#shutil.copyfile(tmpdir+"/"+str(pass_num)+"_0", bigfile+".sort")

if __name__ == "__main__":
	if len(sys.argv) < 3:
		sys.stderr.write("Usage: "+sys.argv[0]+" FILE_TO_SORT TMP_DIR\n")
		exit(1)
	file_to_sort = sys.argv[1]
	tmp_dir  = sys.argv[2]
	sort_big_file(file_to_sort, tmp_dir)

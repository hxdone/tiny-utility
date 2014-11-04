#!/usr/bin/python

import sys
import subprocess
import string

# A simple python program to calculate and output the joinset of two sorted text files.
# Usage: ./join_set.py FILE_A FILE_B
# The join set will be outputted to file_joinset, while the diff set (set_a - set_b) will be output to file_diffset as well. 
# NOTE: We assume that file_a and file_b have already been SORTED IN PYTHON'S WAY (e.g. using sort_file.py in this way)!!!

file_a = ""
file_b = ""
file_joinset = "a_join_b.txt"
file_diffset = "a_minus_b.txt"

if __name__ == "__main__":
	if len(sys.argv) < 3:
		sys.stderr.write("Usage: "+sys.argv[0]+" FILE_A FILE_B\n")
		exit(1)
	file_a = sys.argv[1]
	file_b = sys.argv[2]
	fp_a = open(file_a, "r")
	fp_b = open(file_b, "r")
	fp_join = open(file_joinset, "w")
	fp_diff = open(file_diffset, "w")
	line_b = fp_b.readline()
	line_a = fp_a.readline()
	# We calculate the join set like merge sort, so the element order MUST be consistent with the comparsion.
	while line_b and line_a:
		if line_b < line_a:
			line_b = fp_b.readline()
		elif line_b > line_a:
			fp_diff.write(line_a)
			line_a = fp_a.readline()
		else:
			fp_join.write(line_a)
			line_a = fp_a.readline()
	while line_a:
		fp_diff.write(line_a)
		line_a = fp_a.readline()
	fp_a.close()
	fp_b.close()
	fp_join.close()
	fp_diff.close()
	line_count_b = string.atof(subprocess.Popen("wc -l "+file_b, stdout=subprocess.PIPE ,shell=True).stdout.read().split(" ")[0])
	line_count_a = string.atof(subprocess.Popen("wc -l "+file_a, stdout=subprocess.PIPE ,shell=True).stdout.read().split(" ")[0])
	line_count_join = string.atof(subprocess.Popen("wc -l "+file_joinset, stdout=subprocess.PIPE ,shell=True).stdout.read().split(" ")[0])
	print "#set_a="+str(line_count_b)
	print "#set_b="+str(line_count_a)
	print "#join_set="+str(line_count_join)
	print "#join_set/#set_a="+str(line_count_join/line_count_a)


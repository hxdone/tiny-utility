#!/usr/bin/python

# A simple python program to do random line-sampling on a text file.
# Usage: ./sample.py DATA_FILE SAMPLE_NUM
# DATA_FILE specifies the file to be sampled, and SAMPLE_NUM specifies the number of lines to be sampled.

import random
import string
import sys

class sampler:
	def __init__(self, m):
		self.buf_list = []
		self.sample_no = m
		self.cur_id = 0
	
	def try_next(self, elem):
		self.cur_id = self.cur_id + 1
		if len(self.buf_list) < self.sample_no:
			self.buf_list.append((elem, self.cur_id))
		else:
			replace_pos = random.randint(0, self.cur_id)
			if replace_pos < self.sample_no:
				self.buf_list[replace_pos] = (elem, self.cur_id)
	
	def get_samples(self):
		sys.stderr.write("#data_set: "+str(self.cur_id)+", #sample: "+str(self.sample_no)+"\n")
		self.buf_list.sort(key=lambda x:x[1])
		return self.buf_list
		
if __name__ == "__main__":
	if len(sys.argv) < 3:
		sys.stderr.write("Usage: "+ sys.argv[0] + " DATA_FILE SAMPLE_NUM\n")
		exit(1)
	filepath = sys.argv[1]
	m = string.atoi(sys.argv[2])
	smp = sampler(m)
	fp = open(filepath, "r")
	line = fp.readline()
	while line:
		line = line.strip("\n")
		smp.try_next(line)
		line = fp.readline()
	sample_list = smp.get_samples()
	for i in range(0, len(sample_list)):
		print sample_list[i][0]+"\t"+str(sample_list[i][1])

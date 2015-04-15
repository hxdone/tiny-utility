#!/home/work/.jumbo/bin/python

# Written by huangxiaodong, to calculate the correlation coefficient of two variables.
# Usage: ./correlation.py FILENAME
# Each line in FILENAME must be two numbers separated by '\t'

import sys
import string
import math

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.stderr.write("Usage: "+sys.argv[0]+" FILENAME\n")
        exit(-1)
    fp = open(sys.argv[1], "r")
    num = 0
    sum_x = sum_y = sum_xx = sum_yy = sum_xy = 0.0
    while True:
        line = fp.readline()
        if not line:
            break
        else:
            tokens = line.strip("\n").split("\t")
            if len(tokens) == 2:
                x = string.atof(tokens[0])
                y = string.atof(tokens[1])
                num += 1
                sum_x += x
                sum_y += y
                sum_xx += x*x
                sum_yy += y*y
                sum_xy += x*y
            else:
                sys.stderr.write("[FATAL]IllegalFormat Line:"+line)
                exit(-2)
    avg_x = sum_x / num
    avg_y = sum_y / num
    correlation = (sum_xy + num*avg_x*avg_y - avg_x*sum_y - avg_y*sum_x) / math.sqrt(sum_xx +
            num*avg_x*avg_x - 2*avg_x*sum_x) / math.sqrt(sum_yy + num*avg_y*avg_y -2*avg_y*sum_y)
    print "correlation:"+str(correlation)

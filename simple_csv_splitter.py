import pandas as pd
import os
import math
import argparse

# add CLI arguments
parser = argparse.ArgumentParser()
parser.add_argument('input', metavar='i', type=str, help='input file')
parser.add_argument('output', metavar='o', type=str, help='output path (with no filename)')
parser.add_argument('-d', '--delimiter', help='default comma ","')
parser.add_argument('-r', '--row_limit', help='max row per CSV. Default 100k')
parser.add_argument('-nh', '--no_header', help='set this to 1 to not process headers')

args = vars(parser.parse_args())

# process args
input_file = args['input']
output_path = args['output']
if args['delimiter']:
    delimiter = args['delimiter']
else:
    delimiter = ","
if args['row_limit']:
    row_limit = args['row_limit']
else:
    row_limit = 100000
row_limit = int(row_limit)
if args['no_header']=="1":
    no_header = True
else:
    no_header = False

# rename output path
output_name_template = f"{os.path.split(input_file)[1].split('.')[0]}_output%s.csv"
output_path_full = os.path.join(output_path, output_name_template)

# read and split the file
df = pd.read_csv(input_file, delimiter=delimiter)
chunks = math.ceil(len(df) / row_limit)
dt = {}
for i in range(chunks):
    dt[i] = [row_limit * i, row_limit * (i+1)]
for i in range(chunks):
    df[dt[i][0]:dt[i][1]].to_csv(output_name_template % i, header=not no_header, index=False)

print('Split complete')

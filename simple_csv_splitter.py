import pandas as pd
import os
import math
import argparse

# defaults
input_header = 0
output_header = 1
delimiter = ","
row_limit = 100000

# add CLI arguments
parser = argparse.ArgumentParser()
parser.add_argument('input', metavar='i', type=str, help='input file')
parser.add_argument('output', metavar='o', type=str, help='output path (with no filename)')
parser.add_argument('-d', '--delimiter', help='default comma ","')
parser.add_argument('-r', '--row_limit', help='max row per CSV. Default 100k')
parser.add_argument('-ih', '--input_header', help="0 or 1. If the input has headers or not. Default = 1")
parser.add_argument('-oh', '--output_header', help='0 or 1. To output headers or not. Default = 1')

args = vars(parser.parse_args())

# process args
input_file = args['input']
output_path = args['output']
if args['delimiter']:
    delimiter = args['delimiter']
if args['row_limit']:
    row_limit = int(args['row_limit'])
if args['input_header'] == "1":
    input_header = 0
elif args['input_header'] == "0":
    input_header = None
if args['output_header'] == "1":
    output_header = True
elif args['output_header'] == "0":
    output_header = False

# rename output path
output_name_template = f"{os.path.split(input_file)[1].split('.')[0]}_output%s.csv"
output_path_full = os.path.join(output_path, output_name_template)

# read and split the file
df = pd.read_csv(input_file, delimiter=delimiter, header=input_header)
chunks = math.ceil(len(df) / row_limit)
dt = {}

# write each chunk to a new file
for i in range(chunks):
    dt[i] = [row_limit * i, row_limit * (i + 1)]
    df[dt[i][0]:dt[i][1]].to_csv(output_path_full % i, header=output_header if input_header == 0 else False, index=False)

print('Split complete. Outputted to file: %s' % output_name_template % '', 'Total files=%s' % chunks)

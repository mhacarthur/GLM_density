import os
import glob
import subprocess
import numpy as np
from subprocess import Popen, PIPE

import argparse

from os.path import exists as file_exists

parser = argparse.ArgumentParser()
parser.add_argument("-yr", "--year", type=str, required=True)
parser.add_argument("-mo", "--month", type=str, required=True)

args = vars(parser.parse_args())
year = vars(parser.parse_args())['year']
month = vars(parser.parse_args())['month'].zfill(2)

if len(month) != 2:
    print('ERROR: Month value must be 2 digits')
    exit()

if int(month) < 1 or int(month) > 12:
    print('ERROR: Month value must be between 1 and 12')
    exit()

if len(year) != 4:
    print('ERROR: Year value must be 4 digits')
    exit()

if int(year) < 2018 or int(year) > 2022:
    print('ERROR: Year value must be between 2018 and 2022')
    exit()

if int(year) == 2018 and int(month) < 3:
    print('ERROR: Year 2018 and month < 3 are not available')
    exit()

url_in = 'noaa-goes16/GLM-L2-LCFA/'+ year +'/'+ month

print()
print(f'Year  : {year}')
print(f'Month : {month}')
print(f'url_in: {url_in}')
print()

dir_base = '/home/arturo/Documents/GLM/'
if os.path.isdir(dir_base):
    print(f'{dir_base} exists')
else:
    os.mkdir(dir_base)
    print(f'{dir_base} created')

dir_year = dir_base + str(year)
if os.path.isdir(dir_year):
    print(f'{dir_year} exists')
else:
    os.mkdir(dir_year)
    print(f'{dir_year} created')

dir_out = dir_year + '/' + str(month) + '/'
if os.path.isdir(dir_out):
    print(f'{dir_out} exists')
else:
    os.mkdir(dir_out)
    print(f'{dir_out} created')

print()
print('getting list files')
list_files = subprocess.run(["aws", "s3", "--no-sign-request", "ls", "--recursive", url_in], stdout=PIPE).stdout.splitlines()
len_list_files = len(list_files)
print(f'len_list_files: {len_list_files}')
print()

for nn in range(len_list_files):
    name1 = list_files[nn].decode('utf-8').split()[-1]
    file_download = 's3://noaa-goes16/' + name1
    salida = dir_out + name1.split('/')[-1]
    
    if nn%2000 == 0:
        print(f'{nn}/{len_list_files}')

    if  file_exists(salida) == True:
        pass
    else:
        subprocess.run(["aws", "s3", "--no-sign-request", "cp", file_download, salida])



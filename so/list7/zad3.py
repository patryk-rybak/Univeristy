import os
import sys
import subprocess

if len(sys.argv) > 2 or (len(sys.argv) == 2 and sys.argv[1] != '--verbose'):
	print("Usage:\tpython3 zad3.py [option]\nOptions:\n\t--verbose")
	sys.exit()

verbose = sys.argv[1] == '--verbose' if len(sys.argv) == 2 else False




vmsize = 0
vmrss = 0
for file_name in os.listdir('/proc/'):
    try:
        vmsize += int(subprocess.check_output(f'cat /proc/{file_name}/status | grep VmSize', stderr=subprocess.STDOUT, shell=True).decode('utf-8').split()[1])
        vmrss += int(subprocess.check_output(f'cat /proc/{file_name}/status | grep VmRSS', stderr=subprocess.STDOUT, shell=True).decode('utf-8').split()[1])
        if verbose: print(file_name)
    except:
        continue

print(f'\nVmSize: {vmsize} kb\nVmRSS: {vmrss} kb')


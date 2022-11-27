# import subprocess to run shell commands
import subprocess

# TODO(VG): Add run pytools.py to dockerfile

# Install black and pylint before running this script
subprocess.run(['pip', 'install', 'black', 'pylint'])

# Shell command to run python black (formatter)
output = subprocess.run(['python', '-m', 'black', 'toy.py'], shell=True)

# Shell command to run pylint (lint checker)
output = subprocess.run(['pylint', 'toy.py'], shell=True)

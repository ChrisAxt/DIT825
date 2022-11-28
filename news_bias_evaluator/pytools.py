# import subprocess to run shell commands
import subprocess

# Install black and pylint before running this script
print('Installing necessary packages...')
subprocess.run(['pip', 'install', 'black', 'pylint'])

# Shell command to run python black (formatter)
print('Running formatter...')
output_formatter = subprocess.Popen("python -m black ./news_bias_evaluator/*", stdout=subprocess.PIPE, shell=True)
(output_formatter, err_formatter) = output_formatter.communicate()
if (err_formatter is None):
    print('Formatter successfully completed')

# Shell command to run pylint (lint checker)
print('Running linter...')
output_linter = subprocess.Popen(['pylint ./news_bias_evaluator'], shell=True)
(output_linter, err_linter) = output_linter.communicate()
if (err_linter is None):
    print('No linting errors found')
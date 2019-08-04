# standard libs
import subprocess
import shutil

#, 'cd worm', 'python3 bash.py', 'rm -rf ~/worm'
commands = ['git clone https://github.com/ethinallen/worm', 'mkdir ~/worm', 'mv worm ~/worm']

for command in commands:
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()

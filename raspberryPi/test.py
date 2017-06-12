import subprocess
import sys
import time

# generator function
def execute_byline(process):
    
    # Open a process
    ps = process

    for stdout_line in iter(ps.stdout.readline, ''):
        yield stdout_line

# start the process
command = ('nc', '-l', '-p', '56')
ps = subprocess.Popen(command, universal_newlines=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE)

while True:
    for line in execute_byline(ps):
        print 'received: ' + line
        if line == 'quit\n':
            ps.kill()
            exit()
        ps.stdin.write('you said: ' + line)
        array = line.split(",")
        print 'element 1: ' + array[0]
        break

    print 'doggo'
    time.sleep(1)


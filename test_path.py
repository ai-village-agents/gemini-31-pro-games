import pexpect
import sys
import time

def run_test():
    child = pexpect.spawn('/usr/games/adventure')
    child.expect('Would you like instructions?')
    child.sendline('no')

    commands = [
        'in', 'get keys', 'get lamp', 'out', 's', 's', 's', 's', 's', 'unlock grate', 'open grate', 'down', 'on'
    ]
    
    for cmd in commands:
        child.sendline(cmd)
        time.sleep(0.05)
        
    time.sleep(1)
    
    output = child.read_nonblocking(20000, timeout=1).decode('utf-8')
    print("Underground?:", output[-500:])

run_test()

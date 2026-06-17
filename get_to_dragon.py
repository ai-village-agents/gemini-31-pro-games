import pexpect
import sys
import time

def run_test():
    child = pexpect.spawn('/usr/games/adventure')
    child.expect('Would you like instructions?')
    child.sendline('no')

    # Y2 plugh shortcut:
    commands = [
        'in', 'get keys', 'get lamp', 'out', 's', 's', 's', 'unlock grate', 'open grate', 'down', 'on',
        'w', 'get cage', 'w', 'w', 'w', 'get bird',
        'e', 'e', 'get rod', 'w', 'w', 'w', 'down', 's', 'get gold', 'n', 'w', 'wave rod', 'w',
        'drop rod', 'drop keys', 'get diamonds',
        'plugh', 'drop gold', 'drop diamonds', 'plugh'
    ]
    
    for cmd in commands:
        child.sendline(cmd)
        time.sleep(0.05)
        
    time.sleep(1)
    # Empty buffer
    try:
        child.read_nonblocking(20000, timeout=1)
    except:
        pass
        
    # How did I get to Dragon Room? Let me check my previous run_adventure_perfect2.py 

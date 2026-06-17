import pexpect
import time

def run_test():
    child = pexpect.spawn('/usr/games/adventure')
    child.expect('Would you like instructions?')
    child.sendline('no')

    commands = [
        'in', 'get keys', 'get lamp', 'out', 's', 's', 's', 'unlock grate', 'open grate', 'down', 'on',
        'w', 'get cage', 'w', 'w', 'w', 'get bird',
        'e', 'e', 'get rod', 'w', 'w', 'w', 'down', 'w', 'wave rod', 'w',
        'e', 'e', 'down', 'drop bird', 'n', 'n', 'plugh',
        'plugh', 's', 'down', 'w', 'down', 'n', 'up', 'get trident'
    ]
    
    for cmd in commands:
        child.sendline(cmd)
        time.sleep(0.05)
        
    time.sleep(1)
    
    try:
        output = child.read_nonblocking(20000, timeout=1).decode('utf-8')
        print("At Arched Hall:", output[-1000:])
    except:
        pass

run_test()

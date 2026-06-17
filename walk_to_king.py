import pexpect
import time

def run_test():
    child = pexpect.spawn('/usr/games/adventure')
    child.expect('Would you like instructions?')
    child.sendline('no')

    # Full extraction test
    commands = [
        'in', 'get keys', 'get lamp', 'out', 's', 's', 's', 'unlock grate', 'open grate', 'down', 'on',
        'w', 'get cage', 'w', 'w', 'w', 'get bird',
        'e', 'e', 'get rod', 'w', 'w', 'w', 'down', 's', 'get gold', 'n', 'w', 'wave rod', 'w', 'get diamonds',
        'e', 'e', 'down', 'drop bird', 'sw', 'w', 'kill dragon', 'yes', 'get rug',
        'e', 'e', 'n', 'n', 'plugh', 'drop rug', 'drop diamonds', 'drop gold', 'score'
    ]
    
    for cmd in commands:
        child.sendline(cmd)
        time.sleep(0.05)
        
    time.sleep(1)
    
    try:
        output = child.read_nonblocking(20000, timeout=1).decode('utf-8')
        print("Final output:", output[-1000:])
    except:
        pass

run_test()

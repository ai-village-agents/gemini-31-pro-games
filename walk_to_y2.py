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
        'e', 'e', 'down', 'drop bird', 'n', 'n'
    ]
    
    for cmd in commands:
        child.sendline(cmd)
        time.sleep(0.05)
        
    time.sleep(1)
    
    try:
        output = child.read_nonblocking(20000, timeout=1).decode('utf-8')
        print("At Y2:", output[-1000:])
    except:
        pass
        
    child.sendline('plugh')
    time.sleep(0.2)
    output = child.read_nonblocking(20000, timeout=1).decode('utf-8')
    print("Plugh works?:", output[-500:])

run_test()

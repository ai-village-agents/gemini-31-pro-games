import pexpect
import sys
import time

def run_test():
    child = pexpect.spawn('/usr/games/adventure')
    child.expect('Would you like instructions?')
    child.sendline('no')

    # Careful step by step
    commands = [
        'e', 'in', 'get lamp', 'get keys', 'out', 's', 's', 's', 'unlock grate', 'open grate', 'down', 'on', 'w', 'get cage', 'w', 'w', 'w', 'get bird',
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
        
    child.sendline('s')
    time.sleep(0.1)
    child.sendline('s')
    time.sleep(0.1)
    child.sendline('sw')
    time.sleep(0.1)
    child.sendline('w')
    time.sleep(0.1)
    child.sendline('kill dragon')
    time.sleep(0.1)
    child.sendline('yes')
    time.sleep(0.1)
    child.sendline('get rug')
    time.sleep(0.1)
    
    print("At rug.")
    
    child.sendline('e')
    time.sleep(0.2)
    output = child.read_nonblocking(20000, timeout=1).decode('utf-8')
    print("East:", output[-500:])
    
    child.sendline('e')
    time.sleep(0.2)
    output_e2 = child.read_nonblocking(20000, timeout=1).decode('utf-8')
    print("East 2:", output_e2[-500:])

    child.sendline('n')
    time.sleep(0.2)
    output_n = child.read_nonblocking(20000, timeout=1).decode('utf-8')
    print("North:", output_n[-500:])

    child.sendline('quit')
    child.sendline('y')

run_test()

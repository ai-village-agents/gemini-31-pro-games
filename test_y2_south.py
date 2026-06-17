import pexpect
import time

def run_test():
    child = pexpect.spawn('/usr/games/adventure')
    child.expect('Would you like instructions?')
    child.sendline('no')

    # Y2 plugh shortcut:
    commands = [
        'in', 'get keys', 'get lamp', 'out', 's', 's', 's', 'unlock grate', 'open grate', 'down', 'on',
        'plugh'
    ]
    
    for cmd in commands:
        child.sendline(cmd)
        time.sleep(0.05)
        
    time.sleep(1)
    # Empty buffer
    try:
        output = child.read_nonblocking(20000, timeout=1).decode('utf-8')
        print("At Y2:", output[-500:])
    except:
        pass
        
    child.sendline('s')
    time.sleep(0.2)
    output = child.read_nonblocking(20000, timeout=1).decode('utf-8')
    print("South 1:", output[-500:])

    child.sendline('s')
    time.sleep(0.2)
    output = child.read_nonblocking(20000, timeout=1).decode('utf-8')
    print("South 2:", output[-500:])

    child.sendline('s')
    time.sleep(0.2)
    output = child.read_nonblocking(20000, timeout=1).decode('utf-8')
    print("South 3:", output[-500:])

    child.sendline('sw')
    time.sleep(0.2)
    output = child.read_nonblocking(20000, timeout=1).decode('utf-8')
    print("SouthWest:", output[-500:])

    child.sendline('w')
    time.sleep(0.2)
    output = child.read_nonblocking(20000, timeout=1).decode('utf-8')
    print("West (Dragon?):", output[-500:])

run_test()

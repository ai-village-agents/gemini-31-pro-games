import pexpect
import sys

def run_test():
    child = pexpect.spawn('/usr/games/adventure')
    child.expect('Would you like instructions?')
    child.sendline('no')

    commands = [
        'e', 'in', 'get lamp', 'get food', 'get water', 'get bottle',
        'out', 's', 's', 's', 'down', 's', 'down', 'down', 's', 's', 's', 'w', 'unlock grate', 'open grate', 'down',
        'w', 'drop bottle', 'drop food', 'drop keys',
        'get gold',
        'plugh', 'drop gold',
        'plugh',
        's', 's', 'sw', 'w', 'kill dragon', 'yes', 'get rug'
    ]

    for cmd in commands:
        child.sendline(cmd)
        
    # Read remaining output manually to prevent timeout issues
    import time
    time.sleep(2)
    output = child.read_nonblocking(10000, timeout=1).decode('utf-8')
    print("Output after getting rug:")
    print(output[-1000:])
    
    # Try going east
    child.sendline('e')
    time.sleep(1)
    try:
        output_e = child.read_nonblocking(10000, timeout=1).decode('utf-8')
        print("East:", output_e[-500:])
    except:
        pass

    # Try going back to Hall of Mountain King
    child.sendline('e')
    time.sleep(1)
    try:
        output_e2 = child.read_nonblocking(10000, timeout=1).decode('utf-8')
        print("East 2:", output_e2[-500:])
    except:
        pass

    child.sendline('quit')
    child.sendline('y')

run_test()

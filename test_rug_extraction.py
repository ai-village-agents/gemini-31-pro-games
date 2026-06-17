import pexpect
import sys

def run_test():
    child = pexpect.spawn('/usr/games/adventure')
    child.expect('Would you like instructions?')
    child.sendline('no')
    child.expect('>')

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
        child.expect(['>', pexpect.EOF, pexpect.TIMEOUT])
        
    print("Obtained rug. Now exploring east from Dragon Room.")
    
    # Try going east
    child.sendline('e')
    child.expect(['>', pexpect.EOF, pexpect.TIMEOUT])
    print("East:", child.before.decode('utf-8'))
    
    child.sendline('quit')
    child.sendline('y')

run_test()

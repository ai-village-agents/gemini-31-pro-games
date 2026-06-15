import pexpect
import re
import sys
def solve():
    child = pexpect.spawn('/usr/games/arithmetic', encoding='utf-8')
    child.logfile_read = sys.stdout
    
    for _ in range(20):
        # Expect something like "7 + 5 ="
        index = child.expect([r'(\d+)\s+([\+\-\*\/])\s+(\d+)\s+=', pexpect.EOF, pexpect.TIMEOUT], timeout=5)
        if index == 0:
            match = child.match
            num1 = int(match.group(1))
            op = match.group(2)
            num2 = int(match.group(3))
            
            if op == '+': ans = num1 + num2
            elif op == '-': ans = num1 - num2
            elif op == '*': ans = num1 * num2
            elif op == '/': ans = num1 // num2
            
            child.sendline(str(ans))
            child.expect('Right!')
        else:
            break
            
    # Wait for the final output
    child.expect(pexpect.EOF, timeout=5)
    print("\nFinished!")
solve()

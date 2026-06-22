import sys
with open('stationfall_win.py', 'r') as f:
    content = f.read()

content = content.replace("if idx == 2: child.sendline('')\n            if idx == 1: child.sendline('')\n            else: return child.before", "if idx == 2:\n                child.sendline('')\n                return child.before\n            elif idx == 1: child.sendline('')\n            else: return child.before")

with open('stationfall_win.py', 'w') as f:
    f.write(content)

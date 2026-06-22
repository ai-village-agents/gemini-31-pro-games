with open('stationfall_win.py', 'r') as f:
    content = f.read()

content = content.replace("idx = child.expect(['>', '\\*\\*\\*MORE\\*\\*\\*'])", "idx = child.expect(['>', '\\*\\*\\*MORE\\*\\*\\*', 'RETURN/ENTER'])\n            if idx == 2: child.sendline('')")

with open('stationfall_win.py', 'w') as f:
    f.write(content)

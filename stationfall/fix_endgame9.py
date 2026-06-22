import sys
with open('stationfall_win.py', 'r') as f:
    content = f.read()

content = content.replace("idx = child.expect(['>', '\\*\\*\\*MORE\\*\\*\\*', r'RETURN/ENTER\\\\.\\]'])", "idx = child.expect(['>', '\\*\\*\\*MORE\\*\\*\\*', 'RETURN/ENTER'])")

with open('stationfall_win.py', 'w') as f:
    f.write(content)

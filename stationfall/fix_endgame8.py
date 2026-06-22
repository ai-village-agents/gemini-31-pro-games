import sys
with open('stationfall_win.py', 'r') as f:
    content = f.read()

content = content.replace("idx = child.expect(['>', '\\*\\*\\*MORE\\*\\*\\*', 'RETURN/ENTER\\\\.\]'])", "idx = child.expect(['>', '\\*\\*\\*MORE\\*\\*\\*', r'RETURN/ENTER\\\\.\\]'])\n            # print('DEBUG IDX', idx)")
content = content.replace('print(cmd("SCORE"))', 'print("SCORE:")\nprint(cmd("SCORE"))')

with open('stationfall_win.py', 'w') as f:
    f.write(content)

import re

with open('stationfall_win.py', 'r') as f:
    content = f.read()

content = content.replace('    "UNLOCK BIN", "OPEN BIN",\n', '    "UNLOCK BIN WITH KEY", "OPEN BIN",\n')

with open('stationfall_win.py', 'w') as f:
    f.write(content)


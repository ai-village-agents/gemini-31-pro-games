import sys
with open('stationfall_win.py', 'r') as f:
    content = f.read()

content = content.replace('print(cmd("GET THERMOS"))', 'print(cmd("WAIT"))\nprint(cmd("WAIT"))\nprint(cmd("GET THERMOS"))')

with open('stationfall_win.py', 'w') as f:
    f.write(content)

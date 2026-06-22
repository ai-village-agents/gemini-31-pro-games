with open('stationfall_win.py', 'r') as f:
    content = f.read()

content = content.replace('print(cmd("PUT FOIL ON PYRAMID"))', 'print(cmd(""))\nprint(cmd("PUT FOIL ON PYRAMID"))')

with open('stationfall_win.py', 'w') as f:
    f.write(content)

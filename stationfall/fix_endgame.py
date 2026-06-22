with open('stationfall_win.py', 'r') as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    new_lines.append(line)
    if 'print(cmd("GET UP"))' in line:
        new_lines.append('print(cmd("GET THERMOS"))\n')
        new_lines.append('print(cmd("GET TIMER"))\n')
        new_lines.append('print(cmd("GET DETONATOR"))\n')

with open('stationfall_win.py', 'w') as f:
    f.writelines(new_lines)

with open('/home/computeruse/gemini-31-pro-games/stationfall/stationfall_win.py', 'r') as f:
    content = f.read()

content = content.replace('"ENTER AIR SHAFT"', '"ENTER SHAFT"')

with open('/home/computeruse/gemini-31-pro-games/stationfall/stationfall_win.py', 'w') as f:
    f.write(content)


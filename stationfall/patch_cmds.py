with open('/home/computeruse/gemini-31-pro-games/stationfall/stationfall_win.py', 'r') as f:
    content = f.read()

# Fix the sequence causing the failure
content = content.replace('"REMOVE GRATE", "ENTER AIR SHAFT",', '"REMOVE GRATE", "WAIT", "ENTER AIR SHAFT",')

with open('/home/computeruse/gemini-31-pro-games/stationfall/stationfall_win.py', 'w') as f:
    f.write(content)


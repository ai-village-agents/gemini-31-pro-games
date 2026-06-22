with open('/home/computeruse/gemini-31-pro-games/stationfall/stationfall_win.py', 'r') as f:
    content = f.read()

# Replace the incorrect sequence with just "REMOVE GRATE" and then proceeding DOWN.
content = content.replace('"REMOVE GRATE", "WAIT", "ENTER AIR SHAFT",', '"REMOVE GRATE",')
content = content.replace('"REMOVE GRATE", "ENTER SHAFT",', '"REMOVE GRATE",')

with open('/home/computeruse/gemini-31-pro-games/stationfall/stationfall_win.py', 'w') as f:
    f.write(content)


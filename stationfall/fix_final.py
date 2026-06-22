with open('/home/computeruse/gemini-31-pro-games/stationfall/stationfall_win.py', 'r') as f:
    content = f.read()

# Fix the regex: only match prompt at the end of output, and make sure it's the actual prompt
content = content.replace(r"r'.*ENTER.*'", r"r'\[Hit RETURN or ENTER\.\]'")

# Restore ENTER AIR SHAFT
content = content.replace(
    '"UNLOCK BIN WITH KEY", "OPEN BIN",\n    "GET ZAPGUN", "GET JAMMER", "GET FOIL",\n    "REMOVE GRATE"',
    '"UNLOCK BIN WITH KEY", "OPEN BIN",\n    "GET ZAPGUN", "GET JAMMER", "GET FOIL",\n    "REMOVE GRATE", "ENTER AIR SHAFT", "DOWN", "DOWN", "DOWN", "DOWN", "DOWN", "DOWN", "DOWN", "DOWN",\n    "KICK GRATE", "TURN JAMMER ON", "TURN JAMMER OFF", "UP", "SHOOT FLOYD", "PUT FOIL ON PYRAMID"'
)

with open('/home/computeruse/gemini-31-pro-games/stationfall/stationfall_win.py', 'w') as f:
    f.write(content)


import re

with open('/home/computeruse/gemini-31-pro-games/stationfall/run_stationfall_seed32.py', 'r') as f:
    content = f.read()

# We need to change the commands around "FLOYD, GET BIT"
# It currently is: "SOUTH", "WEST", "WEST", "FLOYD, GET BIT", "GET BIT", "EAST", "NORTH", "NW",
# We should change it so that we WAIT until Floyd is there.
# Since it's a list, it's easier to just split the string, edit it, and write it back.

new_content = content.replace('"SOUTH", "WEST", "WEST", "FLOYD, GET BIT", "GET BIT", "EAST", "NORTH", "NW",', 
    '"SOUTH", "WEST", "WEST", "WAIT", "WAIT", "WAIT", "FLOYD, GET BIT", "GET BIT", "EAST", "NORTH", "NW",')

with open('/home/computeruse/gemini-31-pro-games/stationfall/run_stationfall_seed32.py', 'w') as f:
    f.write(new_content)

import pexpect
import re
child = pexpect.spawn('dfrotz -s 32 /home/computeruse/gemini-31-pro-games/stationfall/s6.z3', encoding='utf-8')
def w():
    idx = child.expect(['>', '\*\*\*MORE\*\*\*'])
    if idx == 1: child.sendline(''); return w()
    return child.before
w()
def cmd(c): child.sendline(c); return w()
def check_moves():
    out = cmd("TIME")
    m = re.search(r'Moves:\s*(\d+)', out)
    return int(m.group(1)) if m else 0

for c in ["EAST", "NORTH", "PUT ROBOT FORM IN SLOT", "TYPE 3", "SOUTH", "EAST",
    "OPEN HATCH", "ENTER TRUCK", "CLOSE HATCH", "SIT ON PILOT SEAT"]: cmd(c)
moves = check_moves()
while moves < 4700:
    cmd("WAIT")
    moves = check_moves()
cmd("PUT SPACECRAFT FORM IN SLOT")
cmd("TYPE 464")
cmd("WAIT")
for i in range(15):
    o = cmd("G")
    if "Stationfall" in o: break

for c in ["GET UP", "DROP FORM", "GET KIT", "OPEN HATCH", "OUT", "EAST", "OPEN KIT", "EAT GOO", "DROP KIT"]: cmd(c)
for c in ["SE", "SE", "EAST", "GET TAPE", "WEST", "PUT TAPE IN READER", "TURN READER ON"]: cmd(c)
for c in ["SOUTH", "WEST", "WEST", "FLOYD, GET BIT", "GET BIT", "EAST", "NORTH", "NW", "DOWN", "DOWN"]: cmd(c)
for c in ["OPEN CAN", "GET FORM", "NW", "GET DRILL", "SE", "UP", "UP", "GET THERMOS", "OPEN THERMOS", "DRINK SOUP", "DROP THERMOS", "SE", "SE", "EAST"]: cmd(c)
print("IN COMMANDER'S OFFICE!")
print(cmd("LOOK"))
for c in ["GET SMALL DRILL BIT", "DROP SMALL DRILL BIT", "PUT MEDIUM BIT IN DRILL", "DRILL SAFE", "DROP DRILL"]: cmd(c)

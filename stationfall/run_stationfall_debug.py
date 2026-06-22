import pexpect
import sys
import time
import re

child = pexpect.spawn('dfrotz /home/computeruse/gemini-31-pro-games/stationfall/s6.z3', encoding='utf-8')
child.logfile = sys.stdout

child.expect('>')

def run_cmd(cmd):
    child.sendline(cmd)
    try:
        idx = child.expect(['>', '\*\*\*MORE\*\*\*'], timeout=2)
        if idx == 1:
            child.sendline('')
            idx2 = child.expect(['>', '\*\*\*MORE\*\*\*'], timeout=2)
            while idx2 == 1:
                child.sendline('')
                idx2 = child.expect(['>', '\*\*\*MORE\*\*\*'], timeout=2)
    except pexpect.TIMEOUT:
        print("Timeout waiting for prompt.")
    except pexpect.EOF:
        print(f"EOF reached after command {cmd}")

run_cmd("TIME")
match = re.search(r'moves is (\d+)', child.before)
if match:
    moves = int(match.group(1))
    while moves > 4550:
        run_cmd("RESTART")
        child.expect('\[Y/N\]')
        child.sendline('Y')
        child.expect('>')
        run_cmd("TIME")
        match = re.search(r'moves is (\d+)', child.before)
        if match:
            moves = int(match.group(1))

commands = [
    "EAST", "NORTH", "PUT ROBOT FORM IN SLOT", "3", "SOUTH", "EAST",
    "OPEN HATCH", "ENTER TRUCK", "CLOSE HATCH", "SIT ON PILOT SEAT",
    "PUT SPACECRAFT FORM IN SLOT"
]

for cmd in commands:
    run_cmd(cmd)

run_cmd("TIME")
match = re.search(r'moves is (\d+)', child.before)
if match:
    moves = int(match.group(1))
    while moves < 4700:
        run_cmd("WAIT")
        run_cmd("TIME")
        match = re.search(r'moves is (\d+)', child.before)
        if match:
            moves = int(match.group(1))

commands = [
    "TYPE 464", "WAIT"
]
for cmd in commands:
    run_cmd(cmd)

for i in range(50):
    run_cmd("G")
    if "docking bay two" in child.before.lower() or "stationfall" in child.before.lower():
        break
    
commands2 = [
    "GET UP", "DROP FORM", "GET KIT", "OPEN HATCH", "OUT", "EAST",
    "OPEN KIT", "DROP KIT",
    "SE", "SE", "EAST", "GET TAPE", "WEST", "PUT TAPE IN READER", "TURN READER ON",
    "SOUTH", "WEST", "WEST", "FLOYD, GET BIT", "GET BIT", "EAST", "NORTH", "NW",
    "DOWN", "DOWN",
    "OPEN CAN", "GET FORM", "NW", "GET DRILL", "SE", "UP", "UP",
    "GET THERMOS", "OPEN THERMOS", "DRINK SOUP",
    "DROP THERMOS", "SE", "SE", "EAST",
    "GET SMALL DRILL BIT", "DROP SMALL DRILL BIT", "PUT MEDIUM BIT IN DRILL", "DRILL SAFE", "DROP DRILL",
    "LOOK UNDER BED", "GET STAMP", "WEST", "NW", "NW", "UP", "UP", "UP",
    "NORTH", "GET DETONATOR", "OPEN DETONATOR", "GET HYPERDIODE", "DROP HYPERDIODE", "SW", "DOWN",
]

for cmd in commands2:
    run_cmd(cmd)

child.close()

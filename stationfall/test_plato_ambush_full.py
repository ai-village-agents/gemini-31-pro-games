import pexpect
import sys
import re

child = pexpect.spawn('dfrotz -s 32 /home/computeruse/gemini-31-pro-games/stationfall/s6.z3', encoding='utf-8', timeout=5)

def wait_prompt():
    while True:
        try:
            idx = child.expect(['>', '\*\*\*MORE\*\*\*'], timeout=5)
            if idx == 1:
                child.sendline('')
            else:
                return child.before
        except pexpect.EOF:
            print(f"EOF Error. Buffer before: {child.before}")
            return child.before

def run_cmd(cmd):
    child.sendline(cmd)
    return wait_prompt()

wait_prompt()
cmds1 = [
    "EAST", "NORTH", "PUT ROBOT FORM IN SLOT", "TYPE 3", "SOUTH", "EAST",
    "OPEN HATCH", "ENTER TRUCK", "CLOSE HATCH", "SIT ON PILOT SEAT",
]
for cmd in cmds1: run_cmd(cmd)

out = run_cmd("TIME")
match = re.search(r'Moves:\s*(\d+)', out)
moves = int(match.group(1)) if match else 0

while moves < 4700:
    run_cmd("WAIT")
    out = run_cmd("TIME")
    match = re.search(r'Moves:\s*(\d+)', out)
    moves = int(match.group(1)) if match else 0

run_cmd("PUT SPACECRAFT FORM IN SLOT")
run_cmd("TYPE 464")
run_cmd("WAIT")

landed = False
for i in range(15):
    out = run_cmd("G")
    if "docking bay two" in out.lower() or "docking bay" in out.lower() or "Stationfall" in out:
        landed = True
        break

if not landed:
    print("FAILED TO LAND")
    sys.exit(1)

cmds_rest = [
    "GET UP", "DROP FORM", "GET KIT", "OPEN HATCH", "OUT", "EAST",
    "OPEN KIT", "EAT GOO", "DROP KIT",
    
    "SE", "SE", "EAST", "GET TAPE", "WEST", "PUT TAPE IN READER", "TURN READER ON",
    
    "SOUTH", "WEST", "WEST", "FLOYD, GET BIT", "GET BIT", "EAST", "NORTH", "NW",
    "DOWN", "DOWN",
    "OPEN CAN", "GET FORM", "NW", "GET DRILL", "SE", "UP", "UP",
    "GET THERMOS", "OPEN THERMOS", "DRINK SOUP",
    "DROP THERMOS", "SE", "SE", "EAST",
    "GET SMALL DRILL BIT", "DROP SMALL DRILL BIT", "PUT MEDIUM BIT IN DRILL", "DRILL SAFE", "DROP DRILL",
    
    "LOOK UNDER BED", "GET STAMP", "WEST", "NW", "NW", "UP", "UP", "UP",
    "NORTH", "GET DETONATOR", "OPEN DETONATOR", "GET HYPERDIODE", "DROP HYPERDIODE", "SW", "DOWN",
    
    "NW", "OPEN PRESSER", "PUT CRUMPLED FORM IN PRESSER", "CLOSE PRESSER", "TURN PRESSER ON",
    "OPEN PRESSER", "TURN PRESSER OFF", "GET FORM",
    "VALIDATE FORM", "DROP STAMP", "EAST", "DOWN", "DOWN", "SE", "SOUTH",
    "PUT FORM IN SLOT", "SOUTH", "SOUTH", "SE", "SW",
    
    "GET CAN", "NE", "NE", "UP", "NW", "LOOK AT CEILING", "OPEN PANEL", "GET OSTRICH NIP",
    "OPEN CAGE", "NE", "SPRAY CAN", "WEST", "SPRAY CAN", "WEST", "SPRAY CAN", "WEST", "SPRAY CAN",
    "SW", "SPRAY CAN", "NW", "SPRAY CAN", "UP", "SPRAY CAN", "UP", "SPRAY CAN",
    "SW", "OPEN PULPIT", "FLIP SWITCH", "SPRAY CAN",
    "GRAB LEASH", "GET STAR", "LET GO OF LEASH", "OPEN STAR", "GET HYPERDIODE",
    "PUT HYPERDIODE IN DETONATOR", "CLOSE DETONATOR", "DROP STAR", "DROP CAN",
    
    "EAST", "DOWN", "DOWN", "SE", "SOUTH", "SOUTH", "SOUTH", "NE", "NE", "SE",
    "GET ID CARD", "PUT CARD IN MACHINE", "TURN MACHINE ON", "TYPE 10", "GET CARD",
    "NW", "SW", "SW", "NORTH", "NORTH", "NORTH", "NW", "DOWN", "SE", "PUT CARD IN READER",
    "NORTH", "GET ZAPGUN", "SOUTH", "WEST", "UP", "SE", "SOUTH", "SOUTH", "SOUTH", "SE", "SOUTH",
    "SHOOT LOCK", "GET COIN", "DROP CARD", "NORTH", "SE", "NW", "NW", "NORTH", "NORTH", "NORTH",
    "NW", "NE", "NE",
    "PUT COIN IN SLOT", "TYPE 6", "PUT NIP IN HOLE", "GET TIMER",
    
    "SW", "EAST",
]

for cmd in cmds_rest:
    print(run_cmd(cmd))
    
print("--- NOW IN COMMANDER'S OFFICE ---")
print(run_cmd("LIE DOWN"))
for i in range(10):
    out = run_cmd("WAIT")
    print(out)
    if "Plato" in out and ("zaps" in out or "stun" in out or "points" in out):
        print("PLATO ATTACKED!")
        break

print(run_cmd("FLOYD, HELP"))
print(run_cmd("GET UP"))

for i in range(10):
    out = run_cmd("WAIT")
    print(out)

child.close()

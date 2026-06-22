import pexpect
import sys
import time
import re

child = pexpect.spawn('dfrotz /home/computeruse/gemini-31-pro-games/stationfall/s6.z3', encoding='utf-8', timeout=5)

def wait_prompt():
    while True:
        idx = child.expect(['>', '\*\*\*MORE\*\*\*'], timeout=5)
        if idx == 1:
            child.sendline('')
        else:
            return child.before

def run_cmd(cmd):
    child.sendline(cmd)
    return wait_prompt()

wait_prompt()

def check_moves():
    out = run_cmd("TIME")
    match = re.search(r'Moves:\s*(\d+)', out)
    if match:
        return int(match.group(1))
    
    # Try looking for "Moves is "
    match2 = re.search(r'is (\d+)', out)
    if match2:
        return int(match2.group(1))
        
    return 0

moves = check_moves()
print(f"Starting moves: {moves}")

while moves > 4550:
    print("Restarting because moves > 4550")
    child.sendline("RESTART")
    child.expect('affirmative')
    child.sendline("Y")
    wait_prompt()
    moves = check_moves()
    print(f"New moves: {moves}")

commands_step1 = [
    "EAST", "NORTH", "PUT ROBOT FORM IN SLOT", "TYPE 3", "SOUTH", "EAST",
    "OPEN HATCH", "ENTER TRUCK", "CLOSE HATCH", "SIT ON PILOT SEAT",
    
]

for cmd in commands_step1:
    print(run_cmd(cmd))

moves = check_moves()
print(f"Moves before wait loop: {moves}")

while moves < 4700:
    run_cmd("WAIT")
    moves = check_moves()
    print(f"Waited, moves: {moves}")

print(run_cmd("PUT SPACECRAFT FORM IN SLOT"))
print(run_cmd("TYPE 464"))
print(run_cmd("WAIT"))

landed = False
for i in range(100):
    out = run_cmd("G")
    if "docking bay two" in out.lower() or "docking bay" in out.lower():
        print("Landed!")
        landed = True
        break
    
if not landed:
    print("Failed to land")
    sys.exit(1)

commands_rest = [
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
    
    "SW", "EAST", "LIE DOWN", "WAIT", "GET UP", "GET ALL", "WEST", "SW", "GET THERMOS",
    "NE", "SE", "EAST", "EAST", "EAST", "EAST", "GET HEADLAMP", "WEAR HEADLAMP",
    "WEST", "SOUTH", "SE", "EAST",
    "TURN WHEEL", "UP", "OPEN LOCKER", "GET SUIT", "WEAR SUIT", "DOWN", "WEST", "WEST", "SE", "DOWN",
    "GET BOOTS", "WEAR BOOTS", "UP", "NW", "DOWN", "OPEN INNER DOOR", "DOWN", "CLOSE INNER DOOR",
    "OPEN OUTER DOOR", "DOWN", "TURN HEADLAMP ON", "GET CYLINDER", "PUT CYLINDER IN THERMOS", "CLOSE THERMOS",
    
    "TURN HEADLAMP OFF", "UP", "CLOSE OUTER DOOR", "OPEN INNER DOOR", "REMOVE SUIT", "DROP SUIT",
    "REMOVE BOOTS", "DROP BOOTS",
    "UP", "SW", "NW", "NORTH", "NORTH", "NORTH", "NW", "GET KIT", "EAT GOO", "DROP KIT",
    "SE", "SE", "EAST", "OPEN THERMOS", "GET EXPLOSIVE",
    "CONNECT TIMER TO DETONATOR", "CONNECT DETONATOR TO EXPLOSIVE", "PUT EXPLOSIVE IN HOLE",
    "DROP TIMER", "DROP DETONATOR", "DROP THERMOS", "TURN HEADLAMP ON", "SET TIMER TO 5", "WEST",
]

for cmd in commands_rest:
    print(run_cmd(cmd))

plato_attacked = False
for i in range(15):
    out = run_cmd("WAIT")
    if "Plato" in out or "stun" in out or "zaps" in out:
        plato_attacked = True
        break

if plato_attacked:
    print(run_cmd("FLOYD, HELP"))
    for i in range(5):
        out = run_cmd("WAIT")
        if "blown" in out or "explodes" in out or "destroyed" in out:
            break
    print(run_cmd("GET ZAPGUN"))
    print(run_cmd("EAST"))
    print(run_cmd("GET KEY"))

commands_end = [
    "WEST", "NW", "NW", "NORTH", "NORTH", "GET JAMMER", "EAST", "NORTH", "NORTH", "UP",
    "GET BOARD", "PUT BOARD IN JAMMER", "SET JAMMER TO 710",
    "DOWN", "SOUTH", "SOUTH", "SOUTH", "SE", "EAST", "EAST", "EAST", "SE",
    "BREAK MIRROR", "GET FOIL",
    
    "NW", "WEST", "WEST", "NW", "WEST", "SW", "UP", "UP", "UP", "UP",
    "UNLOCK BIN", "OPEN BIN",
    
    "GET ZAPGUN", "GET JAMMER", "GET FOIL",
    "REMOVE GRATE", "ENTER AIR SHAFT", "DOWN", "DOWN", "DOWN", "DOWN", "DOWN", "DOWN", "DOWN", "DOWN",
    "KICK GRATE",
    "TURN JAMMER ON", "TURN JAMMER OFF", "UP", "SHOOT FLOYD", "PUT FOIL ON PYRAMID",
]

for cmd in commands_end:
    print(run_cmd(cmd))

print(run_cmd("SCORE"))
child.close()

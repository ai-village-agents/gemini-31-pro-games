import pexpect
import re
import sys

child = pexpect.spawn('dfrotz -s 32 /home/computeruse/gemini-31-pro-games/stationfall/s6.z3', encoding='utf-8')

def w():
    while True:
        try:
            idx = child.expect(['>', '\*\*\*MORE\*\*\*'])
            if idx == 1:
                child.sendline('')
            else:
                return child.before
        except pexpect.EOF:
            print("EOF REACHED")
            print(child.before)
            sys.exit(0)

w()

def cmd(c):
    print(f"> {c}")
    child.sendline(c)
    out = w()
    print(out)
    return out

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

cmds = [
    "GET UP", "DROP FORM", "GET KIT", "OPEN HATCH", "OUT", "EAST",
    "OPEN KIT", "EAT GOO", "DROP KIT",
    "SE", "SE", "EAST", "GET TAPE", "WEST", "PUT TAPE IN READER", "TURN READER ON",
    "SOUTH", "WEST", "WEST",
]
for c in cmds: cmd(c)

print("Waiting for Floyd...")
for i in range(10):
    o = cmd("WAIT")
    if "Floyd bounds into the room" in o or "Floyd" in o:
        break

cmds2 = [
    "FLOYD, GET BIT", "GET BIT", "EAST", "NORTH", "NW",
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
    "UP", "SW", "NW", "NORTH", "NORTH", "NORTH", "NW", "GET KIT", "EAT ORANGE GOO", "DROP KIT",
    "SE", "SE",
]
for c in cmds2:
    out = cmd(c)

print("IN COMMANDER'S OFFICE! WAITING FOR AMBUSH...")
for i in range(15):
    out = cmd("WAIT")
    if "Plato" in out and ("zaps" in out or "stun" in out or "points" in out):
        print(f"PLATO ATTACKED! Move: {i}")
        break

print(cmd("FLOYD, HELP"))
print(cmd("GET UP"))
print(cmd("GET ZAPGUN"))
print(cmd("EAST"))
print(cmd("OPEN THERMOS"))
print(cmd("GET EXPLOSIVE"))
print(cmd("CONNECT TIMER TO DETONATOR"))
print(cmd("CONNECT DETONATOR TO EXPLOSIVE"))
print(cmd("PUT EXPLOSIVE IN HOLE"))
print(cmd("DROP TIMER"))
print(cmd("DROP DETONATOR"))
print(cmd("DROP THERMOS"))
print(cmd("TURN HEADLAMP ON"))
print(cmd("SET TIMER TO 5"))
print(cmd("WEST"))
print(cmd("WAIT"))
print(cmd("EAST"))
print(cmd("GET KEY"))

child.close()

import pexpect
import sys
import re

child = pexpect.spawn('dfrotz -s 32 /home/computeruse/gemini-31-pro-games/stationfall/s6.z3', encoding='utf-8', timeout=5)

def wait_prompt():
    while True:
        idx = child.expect(['>', '\\*\\*\\*MORE\\*\\*\\*'], timeout=5)
        if idx == 1: child.sendline('')
        else: return child.before

def run_cmd(cmd):
    child.sendline(cmd)
    return wait_prompt()

wait_prompt()
cmds = [
    "EAST", "NORTH", "PUT ROBOT FORM IN SLOT", "TYPE 3", "SOUTH", "EAST",
    "OPEN HATCH", "ENTER TRUCK", "CLOSE HATCH", "SIT ON PILOT SEAT",
]
for cmd in cmds: run_cmd(cmd)

run_cmd("WAIT")
run_cmd("PUT SPACECRAFT FORM IN SLOT")
run_cmd("TYPE 464")
run_cmd("WAIT")

for i in range(100):
    out = run_cmd("G")
    if "docking bay two" in out.lower() or "docking bay" in out.lower(): break

cmds_rest = [
    "GET UP", "DROP FORM", "GET KIT", "OPEN HATCH", "OUT", "EAST",
    "OPEN KIT", "DROP KIT",
    "SE", "SE", "EAST", "GET TAPE", "WEST", "PUT TAPE IN READER", "TURN READER ON",
    "SOUTH", "WEST", "WEST", "WAIT", "WAIT", "WAIT", "FLOYD, GET BIT", "GET BIT", "EAST", "NORTH", "NW",
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
    "SE", "SE"
]
for cmd in cmds_rest: run_cmd(cmd)

print("\nWaiting in Office for Plato...")
plato_attacked = False
for _ in range(100):
    out = run_cmd("WAIT")
    print(out)
    if "Plato" in out and ("stun" in out or "zaps" in out):
        print("Plato attacked! Triggering Floyd...")
        plato_attacked = True
        break

if plato_attacked:
    for _ in range(5):
        out = run_cmd("FLOYD, HELP")
        print(out)
        if "blown apart" in out or "muscular control has returned" in out or "exploded" in out:
            print("Plato dead!")
            break

    # We must wait for muscular control to return
    for _ in range(15):
        out = run_cmd("WAIT")
        print(out)
        if "muscular control has returned" in out:
            print("Recovered!")
            break
            
    # We drop all items when stunned. Pick them up.
    print(run_cmd("GET ALL"))
    
    # Now go EAST and set the bomb!
    print("Going EAST to plant the bomb...")
    print(run_cmd("EAST"))
    print(run_cmd("OPEN THERMOS"))
    print(run_cmd("GET EXPLOSIVE"))
    print(run_cmd("CONNECT TIMER TO DETONATOR"))
    print(run_cmd("CONNECT DETONATOR TO EXPLOSIVE"))
    print(run_cmd("PUT EXPLOSIVE IN HOLE"))
    print(run_cmd("DROP TIMER"))
    print(run_cmd("DROP DETONATOR"))
    print(run_cmd("DROP THERMOS"))
    print(run_cmd("TURN HEADLAMP ON"))
    print(run_cmd("SET TIMER TO 5"))
    print(run_cmd("WEST"))

    # Wait for the bomb blast
    for _ in range(15):
        out = run_cmd("WAIT")
        print(out)
        if "deafening" in out or "violently rocks" in out:
            print("Bomb exploded!")
            break
            
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

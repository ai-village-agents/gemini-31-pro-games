import pexpect
import sys
import time
import re

# Load the z-machine binary
child = pexpect.spawn('dfrotz /home/computeruse/gemini-31-pro-games/stationfall/s6.z3', encoding='utf-8')

# Stationfall prompts often have a >, but dfrotz can output a space after.
# Wait for initial prompt
child.expect('>')

# A function to run a command and wait for the prompt
def run_cmd(cmd):
    print(f"Executing: {cmd}")
    child.sendline(cmd)
    try:
        # Match standard prompt or the More prompt which requires pressing Enter
        idx = child.expect(['>', '\*\*\*MORE\*\*\*'], timeout=2)
        if idx == 1:
            # Need to press Enter to continue
            child.sendline('')
            idx2 = child.expect(['>', '\*\*\*MORE\*\*\*'], timeout=2)
            while idx2 == 1:
                child.sendline('')
                idx2 = child.expect(['>', '\*\*\*MORE\*\*\*'], timeout=2)
    except pexpect.TIMEOUT:
        print("Timeout waiting for prompt.")
    
    # print the output for debugging
    # print(child.before)

# It says to wait if the moves number is larger than 4550, and use the RESTART command to start the game over again.
# Stationfall uses the same score/moves system as other Infocom games.
# But there is no simple way to check the moves number directly from the initial prompt without a TIME command.
# "The first thing to do is check the current time, which is given as your number of moves. (Dumb, but true.) If your starting moves number is larger than 4550, use the RESTART command to start the game over again. Keep doing that until you get a starting moves value that's under 4550."
run_cmd("TIME")
match = re.search(r'moves is (\d+)', child.before)
if match:
    moves = int(match.group(1))
    print(f"Starting moves: {moves}")
    while moves > 4550:
        run_cmd("RESTART")
        child.expect('\[Y/N\]')
        child.sendline('Y')
        child.expect('>')
        run_cmd("TIME")
        match = re.search(r'moves is (\d+)', child.before)
        if match:
            moves = int(match.group(1))
else:
    print("Could not find starting moves")

# Walkthrough commands
commands = [
    # STEP 1
    "EAST", "NORTH", "PUT ROBOT FORM IN SLOT", "3", "SOUTH", "EAST",
    "OPEN HATCH", "ENTER TRUCK", "CLOSE HATCH", "SIT ON PILOT SEAT",
    "PUT SPACECRAFT FORM IN SLOT"
]

for cmd in commands:
    run_cmd(cmd)

# "type in the correct course heading. It's time-dependent, so use the WAIT command if necessary to get your moves number in the 4700 to 4749 range."
# Let's write a loop to wait until moves >= 4700
run_cmd("TIME")
match = re.search(r'moves is (\d+)', child.before)
if match:
    moves = int(match.group(1))
    print(f"Current moves before waiting: {moves}")
    while moves < 4700:
        run_cmd("WAIT")
        run_cmd("TIME")
        match = re.search(r'moves is (\d+)', child.before)
        if match:
            moves = int(match.group(1))

# "Type in course code 464 (TYPE 464), then wait until the spacetruck lands... It's fastest to use the WAIT command once, then use the G (short for AGAIN) command until the spacetruck settles to the floor of docking bay two"
commands = [
    "TYPE 464", "WAIT"
]
for cmd in commands:
    run_cmd(cmd)

print("Checking if we've landed")
# Loop G until "docking bay two" or "Stationfall" appears
landed = False
for i in range(50):
    run_cmd("G")
    if "docking bay two" in child.before.lower() or "stationfall" in child.before.lower():
        landed = True
        break
    
print(f"Landed: {landed}")

commands2 = [
    # STEP 2
    "GET UP", "DROP FORM", "GET KIT", "OPEN HATCH", "OUT", "EAST",
    "OPEN KIT", "DROP KIT",
    
    "SE", "SE", "EAST", "GET TAPE", "WEST", "PUT TAPE IN READER", "TURN READER ON",
    
    # STEP 3
    "SOUTH", "WEST", "WEST", "FLOYD, GET BIT", "GET BIT", "EAST", "NORTH", "NW",
    "DOWN", "DOWN",
    "OPEN CAN", "GET FORM", "NW", "GET DRILL", "SE", "UP", "UP",
    "GET THERMOS", "OPEN THERMOS", "DRINK SOUP",
    "DROP THERMOS", "SE", "SE", "EAST",
    "GET SMALL DRILL BIT", "DROP SMALL DRILL BIT", "PUT MEDIUM BIT IN DRILL", "DRILL SAFE", "DROP DRILL",
    
    # STEP 4
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
    
    # STEP 5
    "EAST", "DOWN", "DOWN", "SE", "SOUTH", "SOUTH", "SOUTH", "NE", "NE", "SE",
    "GET ID CARD", "PUT CARD IN MACHINE", "TURN MACHINE ON", "TYPE 10", "GET CARD",
    "NW", "SW", "SW", "NORTH", "NORTH", "NORTH", "NW", "DOWN", "SE", "PUT CARD IN READER",
    "NORTH", "GET ZAPGUN", "SOUTH", "WEST", "UP", "SE", "SOUTH", "SOUTH", "SOUTH", "SE", "SOUTH",
    "SHOOT LOCK", "GET COIN", "DROP CARD", "NORTH", "SE", "NW", "NW", "NORTH", "NORTH", "NORTH",
    "NW", "NE", "NE",
    "PUT COIN IN SLOT", "TYPE 6", "PUT NIP IN HOLE", "GET TIMER",
    
    # STEP 6
    "SW", "EAST", "LIE DOWN", "WAIT", "GET UP", "GET ALL", "WEST", "SW", "GET THERMOS",
    "NE", "SE", "EAST", "EAST", "EAST", "EAST", "GET HEADLAMP", "WEAR HEADLAMP",
    "WEST", "SOUTH", "SE", "EAST",
    "TURN WHEEL", "UP", "OPEN LOCKER", "GET SUIT", "WEAR SUIT", "DOWN", "WEST", "WEST", "SE", "DOWN",
    "GET BOOTS", "WEAR BOOTS", "UP", "NW", "DOWN", "OPEN INNER DOOR", "DOWN", "CLOSE INNER DOOR",
    "OPEN OUTER DOOR", "DOWN", "TURN HEADLAMP ON", "GET CYLINDER", "PUT CYLINDER IN THERMOS", "CLOSE THERMOS",
    
    # STEP 7
    "TURN HEADLAMP OFF", "UP", "CLOSE OUTER DOOR", "OPEN INNER DOOR", "REMOVE SUIT", "DROP SUIT",
    "REMOVE BOOTS", "DROP BOOTS",
    "UP", "SW", "NW", "NORTH", "NORTH", "NORTH", "NW", "GET KIT", "EAT GOO", "DROP KIT",
    "SE", "SE", "EAST", "OPEN THERMOS", "GET EXPLOSIVE",
    "CONNECT TIMER TO DETONATOR", "CONNECT DETONATOR TO EXPLOSIVE", "PUT EXPLOSIVE IN HOLE",
    "DROP TIMER", "DROP DETONATOR", "DROP THERMOS", "TURN HEADLAMP ON", "SET TIMER TO 5", "WEST",
]

for cmd in commands2:
    run_cmd(cmd)

print("Waiting for plato to attack")
# "Now that the safe is blown, two things will happen soon. One is that Plato will attack you with a stun ray, and the other is that the station's lights will go out. Your headlamp is already on, so just wait if necessary until Plato attacks. When he does, ask Floyd to help you (FLOYD, HELP), then wait until Plato gets blown up. Pick your zapgun back up, then go east and get the key from the blown-open safe."
plato_attacked = False
for i in range(15):
    run_cmd("WAIT")
    if "Plato" in child.before or "stun" in child.before or "zaps" in child.before:
        plato_attacked = True
        break

if plato_attacked:
    run_cmd("FLOYD, HELP")
    for i in range(5):
        run_cmd("WAIT")
        if "blown" in child.before or "explodes" in child.before or "destroyed" in child.before:
            break
    run_cmd("GET ZAPGUN")
    run_cmd("EAST")
    run_cmd("GET KEY")

commands3 = [
    # STEP 8
    "WEST", "NW", "NW", "NORTH", "NORTH", "GET JAMMER", "EAST", "NORTH", "NORTH", "UP",
    "GET BOARD", "PUT BOARD IN JAMMER", "SET JAMMER TO 710",
    "DOWN", "SOUTH", "SOUTH", "SOUTH", "SE", "EAST", "EAST", "EAST", "SE",
    "BREAK MIRROR", "GET FOIL",
    
    # STEP 9
    "NW", "WEST", "WEST", "NW", "WEST", "SW", "UP", "UP", "UP", "UP",
    "UNLOCK BIN", "OPEN BIN",
    
    "GET ZAPGUN", "GET JAMMER", "GET FOIL",
    "REMOVE GRATE", "ENTER AIR SHAFT", "DOWN", "DOWN", "DOWN", "DOWN", "DOWN", "DOWN", "DOWN", "DOWN", # it says go down until you reach bottom
    "KICK GRATE",
    "TURN JAMMER ON", "TURN JAMMER OFF", "UP", "SHOOT FLOYD", "PUT FOIL ON PYRAMID",
]

for cmd in commands3:
    run_cmd(cmd)

print("Game should be finished. Looking for score.")
run_cmd("SCORE")
print(child.before)

child.close()

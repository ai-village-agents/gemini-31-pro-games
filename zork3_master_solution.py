import pexpect
import sys
import os
import re

with open("/home/computeruse/gemini-31-pro-games/zork3.step", "r") as f:
    text = f.read()

text = text.split("(You continue \"Zork II\" from the bottom of the endless stairs)")[1]
text = text.replace('\n', ' ')
text = re.sub(r'\([^)]*\)', '', text)
raw_commands = [c.strip() for c in text.split(',')]

commands = []
for c in raw_commands:
    if not c: continue
    for sc in c.split(';'):
        sc = sc.strip()
        if sc:
            if ":" in sc and not "SAY TO DUNGEON MASTER" in sc:
                sc = sc.split(":")[1].strip()
            commands.append(sc)

commands = [c for c in commands if "Jacob Gunness" not in c and "1990" not in c]

processed = []
for c in commands:
    if "du take the ring" in c: continue
    if c.startswith("SPRAY REPELLANT ON MYSELF"): c = "SPRAY REPELLANT ON ME"
    processed.append(c)

commands = []
for c in processed:
    if ";" in c:
        commands.extend([sc.strip() for sc in c.split(";") if sc.strip()])
    else:
        commands.append(c)

idx = commands.index("GET TORCH")
first_part = commands[:idx]
second_part = commands[idx:]

first_part = [
    "GET LAMP", "S", "LIGHT LAMP", "W", "W", "GET BREAD", "E", "E", "E", "NE", "SE", "W", "NE", "WAKE UP OLD MAN", "GIVE BREAD TO OLD MAN", "SW", "W", "S", "S", "S", "TURN OFF LAMP", "DROP LAMP", "JUMP LAKE", "W", "S"
]

child = pexpect.spawn("/usr/games/dfrotz /home/computeruse/infocom-rc2014/DAT/ZORK3.DAT", encoding="utf-8")

def expect_prompt(child):
    while True:
        idx = child.expect([">", "\*\*\*MORE\*\*\*"])
        if idx == 0:
            break
        elif idx == 1:
            child.sendline("")

expect_prompt(child)

print("Executing first part...")
for cmd in first_part:
    child.sendline(cmd)
    expect_prompt(child)

print("Executing second part...")
skip_next_d = False
skip_next_u = False
got_first_can = False
got_first_torch = False
for cmd in second_part:
    if skip_next_d and cmd == "D":
        skip_next_d = False
        continue
    if skip_next_u and cmd == "U":
        skip_next_u = False
        continue

    if cmd == "GET AMULET":
        success = False
        attempts = 0
        while not success and attempts < 10:
            attempts += 1
            print(f"--- DIVE ATTEMPT {attempts} ---")
            child.sendline("D")
            expect_prompt(child)
            res = child.before
            if "Something sparkling in the sand catches your eye." in res:
                print("AMULET FOUND!")
                child.sendline("GET AMULET")
                expect_prompt(child)
                child.sendline("U")
                expect_prompt(child)
                success = True
            elif "There's a tremendous fish here" in res:
                print("FISH FOUND. RETREATING.")
                child.sendline("U")
                expect_prompt(child)
            else:
                print("UNKNOWN LAKE STATE.")
                child.sendline("U")
                expect_prompt(child)
        if not success:
            print("FAILED TO GET AMULET")
            sys.exit(1)
        skip_next_u = True
    elif cmd == "D" and second_part[second_part.index(cmd)+1] == "GET AMULET":
        # The script has 'D', 'GET AMULET'. My logic does 'D' inside the GET AMULET block. So we skip this D.
        skip_next_d = True
        pass 
    elif cmd == "WAIT" and second_part[second_part.index(cmd)-1] in ("GET CAN", "DROP TORCH", "TOUCH TABLE"):
        pass
    else:
        print(f"--- EXECUTING COMMAND: {cmd} ---")
        child.sendline(cmd)
        expect_prompt(child)
        
    if cmd == "GET CAN" and not got_first_can:
        got_first_can = True
        print(f"WAITING AFTER {cmd}...")
        while True:
            child.sendline("WAIT")
            expect_prompt(child)
            text_out = child.before.lower()
            if "machine comes to a halt" in text_out or "halt" in text_out or "stop" in text_out or "zork" in text_out or "year" in text_out or "viewing room" in text_out or "open space" in text_out:
                print(f"MACHINE HALTED: {text_out}")
                break
    elif cmd == "DROP TORCH" and not got_first_torch:
        got_first_torch = True
        print(f"WAITING AFTER {cmd}...")
        while True:
            child.sendline("WAIT")
            expect_prompt(child)
            text_out = child.before.lower()
            if "machine comes to a halt" in text_out or "halt" in text_out or "stop" in text_out or "zork" in text_out or "year" in text_out or "viewing room" in text_out or "open space" in text_out:
                print(f"MACHINE HALTED: {text_out}")
                break

print("Finished. Dumping last few outputs:")
child.sendline("LOOK")
expect_prompt(child)
print(child.before)
child.sendline("SCORE")
expect_prompt(child)
print(child.before)

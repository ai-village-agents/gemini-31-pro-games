import pexpect
import sys
import os
import re

with open("infidel.step", "r") as f:
    text = f.read()

text = text.split("(You start in your tent)")[1]
text = text.replace('\n', ' ')
text = re.sub(r'\([^)]*\)', '', text)
raw_commands = [c.strip() for c in text.split(',')]

commands = []
for c in raw_commands:
    if not c: continue
    for sc in c.split(';'):
        sc = sc.strip()
        if sc:
            commands.append(sc)

processed_commands = []
skip_next = False
for i, c in enumerate(commands):
    if skip_next:
        skip_next = False
        continue
    
    if c == "ROLL STATUE":
        if i + 1 < len(commands) and commands[i+1] in ["NE", "NW", "SE", "SW"]:
            dir = commands[i+1]
            processed_commands.append(f"ROLL STATUE {dir}")
            skip_next = True
        else:
            processed_commands.append(c)
    elif c == "ROLL IT NW":
        processed_commands.append("ROLL STATUE NW")
    elif c == "ROLL STATUE SW":
        processed_commands.append("ROLL STATUE SW")
    elif c == "ROLL STATUE SE":
        processed_commands.append("ROLL STATUE SE")
    elif c == "GET CANTEEN":
        processed_commands.append("GET CANTEEN")
    elif c == "SILVER CHALICE AND GOLDEN CHALICE":
        processed_commands.append("GET SILVER CHALICE")
        processed_commands.append("GET GOLDEN CHALICE")
    elif c == "U     W":
        processed_commands.append("U")
        processed_commands.append("W")
    elif c == "N     PUT BOOK IN LARGE RECESS":
        processed_commands.append("N")
        processed_commands.append("PUT BOOK IN LARGE RECESS")
    elif c == "GET OPAL":
        processed_commands.append("GET OPAL CLUSTER")
    elif c == "RUBY AND EMERALD":
        processed_commands.append("GET RUBY CLUSTER")
        processed_commands.append("GET EMERALD CLUSTER")
    elif c == "AGAIN":
        last_roll = None
        for prev in reversed(processed_commands):
            if prev.startswith("ROLL ") or prev.startswith("PUSH ") or prev.startswith("DIG "):
                last_roll = prev
                break
        if last_roll:
            processed_commands.append(last_roll)
        else:
            processed_commands.append("AGAIN")
    elif c == "TURN ISIS":
        # we need light to see the cover to open it! torch went out
        processed_commands.append("LIGHT MATCH")
        processed_commands.append("TURN ISIS")
    else:
        processed_commands.append(c)

commands = processed_commands
commands = [c.replace("GET ALL BUT HEAD AND STATUE", "GET ALL BUT STATUE") for c in commands]
commands = [c.replace("PICKAXE", "PICK AXE") for c in commands]
commands = [c.replace("OPEN QUARTZ COVER    Jacob Gunness - d.17/4-1990", "OPEN QUARTZ COVER") for c in commands]
commands = [c.replace("og", "AND") for c in commands]
commands = [c.replace("REMOVE FIFTH BRICK AND DROP IT AND SCROLL", "REMOVE FIFTH BRICK AND DROP IT; DROP SCROLL") for c in commands]
new_commands = []
for c in commands:
    if ";" in c:
        new_commands.extend([sc.strip() for sc in c.split(";") if sc.strip()])
    else:
        new_commands.append(c)
commands = new_commands

game_path = os.path.expanduser("~/infocom-rc2014/DAT/INFIDEL.DAT")
child = pexpect.spawn(f"dfrotz {game_path}", encoding='utf-8')
transcript = []

def send_and_wait(cmd):
    if cmd is not None:
        child.sendline(cmd)
    while True:
        idx = child.expect([r"RETURN/ENTER key to begin!", r"\*\*\*MORE\*\*\*", r"\n>", r"\[Please type YES or NO.\]", r"Hit RETURN to continue\.", r"\[Press RETURN or ENTER", pexpect.EOF, pexpect.TIMEOUT], timeout=2)
        transcript.append(child.before)
        if idx == 0:
            child.sendline("")
        elif idx == 1:
            child.sendline("")
        elif idx == 2:
            transcript.append("\n>")
            break
        elif idx == 3:
            child.sendline("YES")
        elif idx == 4:
            child.sendline("")
        elif idx == 5:
            child.sendline("")
        else:
            break

send_and_wait(None)
for i, c in enumerate(commands):
    send_and_wait(c)

# Force flush the final state
idx = child.expect([r"\n>", pexpect.EOF, pexpect.TIMEOUT], timeout=2)
transcript.append(child.before)

send_and_wait("quit")
send_and_wait("Y")

with open("infidel-win.txt", "w") as f:
    f.write("".join(transcript))

# Check for win
import hashlib
win_text = "".join(transcript)
if "rank of a master adventurer" in win_text:
    print("WIN DETECTED! Sha256 receipt:")
    print(hashlib.sha256(win_text.encode('utf-8')).hexdigest())
    with open("infidel_receipt.txt", "w") as f:
        f.write(hashlib.sha256(win_text.encode('utf-8')).hexdigest() + "\n")
else:
    print("No master adventurer found in transcript.")

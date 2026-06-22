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
    print(f"CMD: {cmd}")
    child.sendline(cmd)
    out = wait_prompt()
    print(out)
    return out

wait_prompt()
cmds1 = [
    "EAST", "NORTH", "PUT ROBOT FORM IN SLOT", "TYPE 3", "SOUTH", "EAST",
    "OPEN HATCH", "ENTER TRUCK", "CLOSE HATCH", "SIT ON PILOT SEAT",
]
for cmd in cmds1:
    run_cmd(cmd)

out = run_cmd("TIME")
match = re.search(r'Moves:\s*(\d+)', out)
moves = int(match.group(1)) if match else 0
print(f"Moves: {moves}")

while moves < 4700:
    run_cmd("WAIT")
    out = run_cmd("TIME")
    match = re.search(r'Moves:\s*(\d+)', out)
    moves = int(match.group(1)) if match else 0

run_cmd("PUT SPACECRAFT FORM IN SLOT")
run_cmd("TYPE 464")
run_cmd("WAIT")

for i in range(15):
    run_cmd("G")
    
run_cmd("GET UP")
run_cmd("DROP FORM")
run_cmd("GET KIT")
run_cmd("OPEN HATCH")
run_cmd("OUT")

child.close()

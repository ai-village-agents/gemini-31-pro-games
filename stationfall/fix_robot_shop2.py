import pexpect
import sys

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
    "WAIT", "PUT SPACECRAFT FORM IN SLOT", "TYPE 464", "WAIT"
]
for cmd in cmds: run_cmd(cmd)

for i in range(100):
    out = run_cmd("G")
    if "docking bay two" in out.lower() or "docking bay" in out.lower(): break

cmds_rest = [
    "GET UP", "DROP FORM", "GET KIT", "OPEN HATCH", "OUT", "EAST",
    "OPEN KIT", "DROP KIT",
    "SE", "SE", "EAST", "GET TAPE", "WEST", "PUT TAPE IN READER", "TURN READER ON",
    "SOUTH", "WEST", "WEST"
]
for cmd in cmds_rest: run_cmd(cmd)

print("In Robot Shop. Waiting for Plato to wake up Oliver...")
for i in range(30):
    out = run_cmd("WAIT")
    print(out)
    if "reaches over" in out or "sits up" in out or "book" in out:
        pass

print(run_cmd("FLOYD, GET BIT"))
print(run_cmd("GET BIT"))
print(run_cmd("EAST"))
for i in range(3):
    print(run_cmd("WAIT"))

child.close()

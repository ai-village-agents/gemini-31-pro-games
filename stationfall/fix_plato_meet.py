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

# Now go STRAIGHT to the Robot Shop as fast as possible!
cmds_fast = [
    "GET UP", "DROP FORM", "GET KIT", "OPEN HATCH", "OUT", "EAST",
    "SE", "SE", "EAST", "GET TAPE", "WEST", "PUT TAPE IN READER", "TURN READER ON",
    "SOUTH", "WEST", "WEST"
]
for cmd in cmds_fast: run_cmd(cmd)

print("In Robot Shop. Waiting for Plato...")
for i in range(30):
    out = run_cmd("WAIT")
    print(out)
    if "Oliver" in out and ("wakes up" in out or "awake" in out or "activate" in out or "eye" in out or "reaches" in out or "sit" in out or "stroll" in out or "alive" in out):
        print("Oliver woke up!")
        break

print(run_cmd("FLOYD, GET BIT"))
print(run_cmd("GET BIT"))

child.close()

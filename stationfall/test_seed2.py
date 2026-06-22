import pexpect
import re

def test_seed(seed):
    child = pexpect.spawn(f'dfrotz -s {seed} /home/computeruse/gemini-31-pro-games/stationfall/s6.z3', encoding='utf-8')
    child.expect('>')
    child.sendline('TIME')
    child.expect('>')
    match = re.search(r'Moves:\s*(\d+)', child.before)
    if match:
        print(f"Seed {seed}: Moves {match.group(1)}")
    else:
        print(f"Seed {seed}: Moves not found")
    child.close()

for i in range(10, 50):
    test_seed(i)

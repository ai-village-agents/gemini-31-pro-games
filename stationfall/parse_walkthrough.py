import re
with open('walkthrough.txt', 'r') as f:
    text = f.read()

# Try to extract the walkthrough part.
# Let's search for "Part 1" or similar
start = text.find('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
if start == -1:
    print("Could not find start")

text = text[start:]

commands = []
for line in text.split('\n'):
    line = line.strip()
    if line.startswith('- '):
        cmd = line[2:]
        if ' (' in cmd:
            cmd = cmd[:cmd.find(' (')]
        commands.append(cmd.strip())

with open('commands.txt', 'w') as f:
    for cmd in commands:
        f.write(f"{cmd}\n")

print(f"Extracted {len(commands)} commands.")

with open("walkthrough.txt", "r") as f:
    lines = f.readlines()
    
start = -1
for i, line in enumerate(lines):
    if "Wait for Plato to zap you" in line or "Wait for Plato" in line or "WAIT (until Plato appears" in line or "WAIT (wait for Plato to arrive)" in line.lower() or "plato" in line.lower() and "wait" in line.lower():
        start = i - 5
        break

if start == -1:
    print("Could not find the start point. Let's look for 'plato'")
    for i, line in enumerate(lines):
        if "plato" in line.lower():
            print(f"Line {i}: {line.strip()}")
else:
    for line in lines[start:start+50]:
        print(line.strip())

with open('/home/computeruse/gemini-31-pro-games/stationfall/run_stationfall_seed32.py', 'r') as f:
    content = f.read()

old_code = """
if plato_attacked:
    print(run_cmd("FLOYD, HELP"))
    for i in range(5):
        out = run_cmd("WAIT")
        if "blown" in out or "explodes" in out or "destroyed" in out:
            break
    print(run_cmd("GET ZAPGUN"))
    print(run_cmd("EAST"))
    print(run_cmd("GET KEY"))
"""

new_code = """
if plato_attacked:
    print(run_cmd("FLOYD, HELP"))
    for i in range(15):
        out = run_cmd("WAIT")
        if "deafening" in out or "violently rocks" in out or "from the east" in out:
            print("Bomb exploded!")
            break
    print(run_cmd("GET ZAPGUN"))
    print(run_cmd("EAST"))
    print(run_cmd("GET KEY"))
"""

content = content.replace(old_code.strip(), new_code.strip())

with open('/home/computeruse/gemini-31-pro-games/stationfall/run_stationfall_seed32.py', 'w') as f:
    f.write(content)

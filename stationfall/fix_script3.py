with open('/home/computeruse/gemini-31-pro-games/stationfall/run_stationfall_seed32.py', 'r') as f:
    content = f.read()

# Fix EAT GOO
content = content.replace('"GET KIT", "EAT GOO", "DROP KIT"', '"GET KIT", "EAT ORANGE GOO", "DROP KIT"')

# Fix the Plato attack wait loop
old_code = """
plato_attacked = False
for i in range(15):
    out = run_cmd("WAIT")
    if "deafening" in out or "violently rocks" in out or "from the east" in out:
        print("Bomb exploded!")
        break
"""

new_code = """
plato_attacked = False
out = ""
# We just went WEST into the Commander's office. Plato stuns us here.
# The timer is ticking down. 
# We WAIT until we see Plato raise the stun ray, which triggers FLOYD HELP.
for i in range(15):
    out = run_cmd("WAIT")
    if "raises the stun ray" in out or "stun" in out or "zaps" in out or "please don't" in out:
        plato_attacked = True
        break
"""

content = content.replace(old_code.strip(), new_code.strip())

with open('/home/computeruse/gemini-31-pro-games/stationfall/run_stationfall_seed32.py', 'w') as f:
    f.write(content)

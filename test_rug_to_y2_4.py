import pexpect

def explore_from_mirror(cmd):
    child = pexpect.spawn('/usr/games/adventure', encoding='utf-8', timeout=2)
    child.expect('Would you like instructions\?')
    child.sendline('n')
    
    commands = [
        "in", "get lamp", "get keys", "out",
        "south", "south", "south", "unlock grate", "open grate",
        "down", "on", "west", "get cage", "west", "west", "west", "get bird",
        "east", "east", "get rod", "west", "west", "west",
        "down", "south", "get gold", "north", "west", "wave rod", "west",
        "drop rod", "drop keys", "get diamonds",
        "west", "west", "west", "north", "east",
        "get coins", "east", "drop bird", "drop cage", "south", "get jewelry", "north",
        "north", "get silver", "north", "plugh", "drop coins", "drop gold", "drop silver", "drop jewelry", "drop diamonds",
        "plugh", "s", "s", "sw", "w", "kill dragon", "yes", "get rug", "n", "n", cmd, "look"
    ]
    
    for c in commands:
        child.sendline(c)
        text = ""
        while True:
            try:
                child.expect('.+', timeout=0.1)
                text += child.match.group(0)
            except:
                break
        if c == "look":
            print(f"[{cmd}] -> {text.strip().splitlines()[-2:] if len(text.strip().splitlines()) >= 2 else text.strip()}")
    child.close()

if __name__ == "__main__":
    for d in ["n", "s", "e", "w"]:
        explore_from_mirror(d)

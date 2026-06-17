import pexpect
import sys

def run_game():
    child = pexpect.spawn('/usr/games/adventure', encoding='utf-8', timeout=2)
    
    child.expect('Would you like instructions\\?')
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
        "plugh", "s", "down", "w", "down", "w", "w", "oriental", "n", "look"
    ]
    
    for cmd in commands:
        child.sendline(cmd)
        text = ""
        while True:
            try:
                child.expect('.+', timeout=0.1)
                text += child.match.group(0)
            except pexpect.TIMEOUT:
                break
            except pexpect.EOF:
                break
        if cmd == "look":
            print(f"[{cmd}]\\n{text}")

if __name__ == "__main__":
    run_game()

import pexpect
import sys

def run_game():
    child = pexpect.spawn('/usr/games/adventure', encoding='utf-8', timeout=2)
    child.logfile_read = sys.stdout
    
    child.expect('Would you like instructions\\?')
    child.sendline('n')
    
    commands = [
        "in", "get lamp", "get keys", "out", 
        "south", "south", "south", "unlock grate", "open grate", 
        "down", "on", "west", "get cage", "west", "west", "west", "get bird",
        "east", "east", "get rod", "west", "west", "west", 
        "drop lamp"
    ]
    
    for cmd in commands:
        child.sendline(cmd)
        while True:
            try:
                child.expect('.+', timeout=0.5)
            except pexpect.TIMEOUT:
                break
            except pexpect.EOF:
                break

    print("\n--- Now we dropped lamp in Alcove ---")
    commands2 = [
        "east", "drop rod", "drop cage", "drop bird", "east", "east", "down", "south", "get gold", "north",
        "east", "get coins", "east", "south", "get jewelry", "north", "north", "get silver", "north",
        "plugh", "plover", "get emerald", "west", "look", "get lamp", "up"
    ]
    for cmd in commands2:
        print(f"\n--- Trying {cmd} ---")
        child.sendline(cmd)
        while True:
            try:
                child.expect('.+', timeout=0.5)
            except pexpect.TIMEOUT:
                break
            except pexpect.EOF:
                break

if __name__ == "__main__":
    run_game()

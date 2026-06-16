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
            "down", "south", "get gold", "north", "west", "wave rod", "west", 
            "drop rod", "drop keys", "get diamonds",
            "west", "west", "west", "north", "east", 
            "get coins", "east", "drop bird", "drop cage", "south", "get jewelry", "north",
            "north", "get silver", "north",
            "plugh", "plover"
    ]
    
    for cmd in commands:
        child.sendline(cmd)
        try:
            child.expect('>', timeout=1)
        except pexpect.TIMEOUT:
            pass
            
    print("\n--- Now in Plover Room? ---")
    for d in ['n', 's', 'e', 'w', 'ne', 'nw', 'se', 'sw', 'u', 'd', 'out', 'look', 'i']:
        print(f"\n--- Trying {d} ---")
        child.sendline(d)
        try:
            child.expect('>', timeout=1)
        except pexpect.TIMEOUT:
            pass

if __name__ == "__main__":
    run_game()

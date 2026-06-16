import pexpect
import sys

def run_game():
    child = pexpect.spawn('/usr/games/adventure', encoding='utf-8', timeout=2)
    child.logfile_read = sys.stdout
    
    child.expect('Would you like instructions\\?')
    child.sendline('n')
    
    commands = [
        "e", "in", "get lamp", "get keys", "get food", "get water", 
        "out", "s", "s", "s", "s", "s", "s", "s", "s", "s", "s", "s", "s",
        "unlock grate", "open grate", "down", "on", "d", "w",
        "get rod", "w", "w", "get bird", "e", "e", "e", "n", "n", "n", 
        "get coins", "s", "s", "s", "e", "e", "w", "w", "e", "s", "w", "w", 
        "w", "n", "s", "w", "s", "get diamonds", "n", "e", "s", "e", 
        "n", "get silver", "n", "plugh", "drop coins", "drop diamonds", "drop silver", "drop keys", "drop food", "drop water", "drop bird", "drop rod", "plover"
    ]
    
    for cmd in commands:
        child.sendline(cmd)
        try:
            child.expect('>', timeout=1)
        except pexpect.TIMEOUT:
            pass
            
    print("\n--- Now in Plover Room ---")
    
    # Try different directions from Plover room to map the exit
    for d in ['n', 's', 'e', 'w', 'ne', 'nw', 'se', 'sw', 'u', 'd', 'out']:
        print(f"\n--- Trying {d} ---")
        child.sendline(d)
        try:
            child.expect('>', timeout=1)
        except pexpect.TIMEOUT:
            pass

if __name__ == "__main__":
    run_game()

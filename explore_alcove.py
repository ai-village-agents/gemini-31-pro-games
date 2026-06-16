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
                
        text = child.before if child.before else ""
        if child.match:
            text += child.match.group(0)

    print("\n--- Now in Alcove ---")
    for d in ['crack', 'enter crack', 'east', 'e', 'w', 'ne', 'nw']:
        print(f"\n--- Trying {d} ---")
        child.sendline(d)
        try:
            child.expect('>', timeout=1)
        except pexpect.TIMEOUT:
            pass

if __name__ == "__main__":
    run_game()

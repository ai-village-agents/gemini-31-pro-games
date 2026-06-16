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
        "west", "west", "west", "north" # We are now at crossover
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
            
        if "little dwarf" in text and ("threatening" in text or "blocks your way" in text or "after you" in text):
             while True:
                 child.sendline("throw axe")
                 child.expect('.+', timeout=1.0)
                 res = child.match.group(0)
                 if "You killed a little dwarf" in res or "I see no axe here" in res:
                     break
                 elif "misses" in res or "already" in res:
                     pass
                 else:
                     break

    print("\n--- Map to Alcove ---")
    route = [
        "east", "east", "south" # From crossover, east to west side chamber, east to Hall of Mt King, south to South side chamber?
    ]

    for cmd in route:
        print(f"\n--- Cmd {cmd} ---")
        child.sendline(cmd)
        try:
            child.expect('>', timeout=1)
        except pexpect.TIMEOUT:
            pass

    child.interact()

if __name__ == "__main__":
    run_game()

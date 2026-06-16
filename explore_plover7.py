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
        "north", "get silver", "north", "plugh", "drop coins", "drop gold", "drop silver", "drop jewelry", "drop diamonds",
        "plugh", "plover"
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
                 if "There is a little axe here" in text:
                     child.sendline("get axe")
                     child.expect('.+', timeout=0.5)
                 child.sendline("throw axe")
                 child.expect('.+', timeout=1.0)
                 res = child.match.group(0)
                 if "You killed a little dwarf" in res:
                     break
                 elif "misses" in res or "already" in res:
                     pass
                 else:
                     break
                     
    print("\n--- Now in Plover Room ---")
    for d in ['get emerald', 'plover', 'plover']:
        print(f"\n--- Trying {d} ---")
        child.sendline(d)
        try:
            child.expect('>', timeout=1)
        except pexpect.TIMEOUT:
            pass


if __name__ == "__main__":
    run_game()

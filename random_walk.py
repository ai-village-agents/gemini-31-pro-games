import pexpect
import random
import sys
import collections

def explore():
    child = pexpect.spawn('/usr/games/adventure', encoding='utf-8')
    
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
        "plugh", "south", "south", "west", "west", "south"
    ]
    for cmd in commands:
        child.sendline(cmd)
        while True:
            try:
                child.expect('.+', timeout=0.1)
            except pexpect.TIMEOUT:
                break
            except pexpect.EOF:
                break

    directions = ["north", "south", "east", "west", "ne", "nw", "se", "sw", "up", "down"]
    path = []
    
    for i in range(50):
        d = random.choice(directions)
        child.sendline(d)
        
        while True:
            try:
                child.expect('.+', timeout=0.2)
            except pexpect.TIMEOUT:
                break
            except pexpect.EOF:
                break
                
        text = child.before if child.before else ""
        if child.match:
            text += child.match.group(0)
            
        if "little dwarf" in text:
             child.sendline("throw axe")
             while True:
                 try:
                     child.expect('.+', timeout=0.2)
                 except:
                     break

        path.append(d)
        
        if "Bedquilt" in text or "Complex" in text or "Alcove" in text or "Swiss Cheese" in text:
            print(f"FOUND IT: {text}")
            print(f"Path taken: {path}")
            return path
            
        if "killed" in text and "reincarnate" in text:
            return None
            
    child.close()
    return None

if __name__ == "__main__":
    for i in range(100):
        print(f"Attempt {i}...")
        res = explore()
        if res:
            break

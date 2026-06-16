import pexpect
import sys

def main():
    child = pexpect.spawn('/usr/games/adventure', encoding='utf-8')
    child.timeout = 2
    
    def send(cmd):
        child.sendline(cmd)
        buffer = ""
        while True:
            try:
                child.expect('.+', timeout=0.5)
                buffer += child.match.group(0)
            except pexpect.TIMEOUT:
                break
            except pexpect.EOF:
                break
        
        lines = [line.strip() for line in buffer.split('\r\n') if line.strip()]
        if lines and lines[0] == cmd:
            lines = lines[1:]
        
        text = " ".join(lines)
        if lines:
            print(f"> {cmd}")
            for line in lines:
                print(f"  {line}")
                
        # Dwarf combat check
        if "little dwarf" in text and ("threatening" in text or "blocks your way" in text or "after you" in text):
            print("\n[ COMBAT ENGAGED ]")
            while True:
                if "There is a little axe here" in text:
                    child.sendline("get axe")
                    child.expect('.+', timeout=0.5)
                
                child.sendline("throw axe")
                child.expect('.+', timeout=1.0)
                res = child.match.group(0)
                print(f"  {res.strip()}")
                if "You killed a little dwarf" in res:
                    print("[ DWARF KILLED ]")
                    break
                elif "misses" in res or "already" in res:
                    pass
                else:
                    break
                
        return text

    for cmd in ["no", "enter", "get lamp", "get keys", "get water", "out", 
                "south", "south", "south", "unlock grate", "open grate", 
                "down", "on", "west", "get cage", "west", "west", "west", "get bird",
                "east", "east", "get rod",
                "west", "west", "west", "down", "west", "wave rod", "west", "get diamonds",
                "east", "east", "down", "drop bird", "drop cage", "drop rod", 
                "south", "get jewelry", "north", "west", "get coins", "east", "north", "get silver",
                "south", "east", "up", "up", "east", "east", "east", "xyzzy",
                "drop diamonds", "drop jewelry", "drop coins", "drop silver"]:
        send(cmd)

    print("\n[ GOING FOR GOLD ]")
    for cmd in ["xyzzy", "west", "west", "west", "down", "south"]:
        send(cmd)
        
    print("\n[ EXPLORING GOLD ESCAPE ROUTE ]")
    send("get gold")
    # Where does the gold room lead? The description says "low room". 
    # What directions are there?
    send("look")
    
    # Try East, West, South, Down from Gold room
    send("east")
    send("west")
    send("south")
    send("down")
    
    # If no way out, just drop gold and quit.
    send("drop gold")
    send("score")

    child.sendline("quit")
    child.sendline("y")
    
if __name__ == '__main__':
    main()

import pexpect
import sys

def main():
    child = pexpect.spawn('/usr/games/adventure', encoding='utf-8')
    child.timeout = 2
    
    with open('/home/computeruse/gemini-31-pro-games/adventure_107_run.txt', 'w') as f:
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
                f.write(f"> {cmd}\n")
                print(f"> {cmd}")
                for line in lines:
                    f.write(f"  {line}\n")
                    print(f"  {line}")
                    
            if "little dwarf" in text and ("threatening" in text or "blocks your way" in text or "after you" in text):
                while True:
                    if "There is a little axe here" in text:
                        child.sendline("get axe")
                        child.expect('.+', timeout=0.5)
                    child.sendline("throw axe")
                    child.expect('.+', timeout=1.0)
                    res = child.match.group(0)
                    f.write(f"  {res.strip()}\n")
                    if "You killed a little dwarf" in res:
                        break
                    elif "misses" in res or "already" in res:
                        pass
                    else:
                        break
            return text

        commands = [
            "no", "enter", "get lamp", "get keys", "get water", "out", 
            "south", "south", "south", "unlock grate", "open grate", 
            "down", "on", "west", "get cage", "west", "west", "west", "get bird",
            "east", "east", "get rod",
            "west", "west", "west", "down", "west", "wave rod", "west", "get diamonds",
            "east", "east", "down", "drop bird", "drop cage", "drop rod", 
            "south", "get jewelry", "north", "west", "get coins", "east", "north", "get silver",
            "south", "east", "up", "up", "east", "east", "east", "xyzzy",
            "drop diamonds", "drop jewelry", "drop coins", "drop silver", "score", "quit", "y"
        ]

        for cmd in commands:
            send(cmd)

if __name__ == '__main__':
    main()

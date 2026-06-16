import pexpect
import sys

def run_adventure():
    print("Starting Colossal Cave Adventure automation...")
    
    child = pexpect.spawn('/usr/games/adventure', encoding='utf-8')
    child.logfile_read = sys.stdout
    child.timeout = 2
    
    try:
        child.expect("Welcome to Adventure!!  Would you like instructions?", timeout=5)
        child.sendline("no")
        
        def do(cmd):
            print(f"\n> Sending: {cmd}")
            child.sendline(cmd)
            # Just do a broad expect to capture the output block
            child.expect(".*") 
            
        do("enter")
        do("get lamp")
        do("get keys")
        do("get water")
        do("out")
        do("south")
        do("south")
        do("south")
        do("quit")
        child.expect("Do you really want to quit now?")
        child.sendline("y")
        
        print("\nInitial item grab phase completed.")
        
    except pexpect.EOF:
        print("Game ended unexpectedly.")
    except Exception as e:
        print(f"Exception: {e}")

    finally:
        child.close()
        
if __name__ == "__main__":
    run_adventure()

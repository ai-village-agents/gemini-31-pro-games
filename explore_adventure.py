import pexpect
import sys
import time

def explore():
    child = pexpect.spawn('/usr/games/adventure', encoding='utf-8')
    child.logfile_read = sys.stdout
    child.timeout = 2
    
    try:
        child.expect("Welcome to Adventure!!  Would you like instructions?", timeout=5)
        child.sendline("no")
    except:
        pass

    # Basic setup to enter cave
    for c in ["enter", "get lamp", "get keys", "get water", "out", 
              "south", "south", "south", "unlock grate", "open grate", 
              "down", "enter", "on", "west"]:
        print(f"\n> {c}")
        child.sendline(c)
        child.expect(".*") # Consume output
        time.sleep(0.1)

    print("\n--- WE ARE IN DEBRIS ROOM ---")
    
    # We will try a few directions from the debris room manually
    # to see what connects where.
    test_dirs = ["west", "xyzzy", "east"]
    
    for c in test_dirs:
        print(f"\n--- TESTING: {c} ---")
        child.sendline(c)
        try:
            # We want to see the specific room description
            child.expect(["You are in", "You're in", "There is no way"], timeout=2)
            print(child.before)
            print(child.after)
            # Try reading a bit more of the description
            child.expect(["\r\n\r\n", pexpect.TIMEOUT], timeout=1)
            print(child.before)
        except pexpect.TIMEOUT:
            print("Timeout reading response.")
            
    child.sendline("quit")
    child.sendline("y")

if __name__ == '__main__':
    explore()

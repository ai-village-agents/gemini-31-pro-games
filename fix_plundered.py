import pexpect
import sys
import time

def run_game():
    cmds_file = '/home/computeruse/opus-47-games/day-441/plundered-hearts/walk.cmds'
    dat_file = '/home/computeruse/infocom-rc2014-temp/DAT/PLUNDERE.DAT'
    
    with open(cmds_file, 'r') as f:
        commands = [line.strip() for line in f if line.strip()]

    # To fix Plundered Hearts desync: insert "wait" before the "yes" response
    # at the final beach sequence when Lafond pulls a pistol (turn ~232).
    # Since we can't easily track narrative, just pad the "yes" with spaces 
    # to create delays, or inject waits where needed based on the commands buffer.
    fixed_commands = []
    for cmd in commands:
        if cmd == "yes":
            # Add some padding to make sure the game catches up to the narrative prompt
            fixed_commands.append("wait")
            fixed_commands.append("wait")
        fixed_commands.append(cmd)
            
    child = pexpect.spawn(f'dfrotz -m {dat_file}', encoding='utf-8')
    child.logfile_read = sys.stdout
    
    # Wait for the initial prompt
    child.expect(r'>', timeout=5)

    full_output = ""

    for i, cmd in enumerate(fixed_commands):
        child.sendline(cmd)
        
        while True:
            # Handle prompt variations
            index = child.expect([r'>', r'Do you want to keep waiting\?', r'\[Please type YES or NO\.\]', r'\[Press RETURN or ENTER to begin\.\]', r'\[Press RETURN or ENTER to continue\.\]', pexpect.EOF, pexpect.TIMEOUT], timeout=3)
            full_output += child.before
            if index == 0:
                if "[Please type YES or NO.]" in child.before:
                    child.sendline("yes")
                    continue
                else:
                    break
            elif index == 1:
                child.sendline("yes")
            elif index == 2:
                child.sendline("yes")
            elif index == 3:
                child.sendline("")
            elif index == 4:
                child.sendline("")
            elif index == 5:
                print("\nReached EOF.")
                return
            elif index == 6:
                break
                
    try:
        child.expect(pexpect.EOF, timeout=2)
    except:
        pass
        
    full_output += child.before
    if "Your score is 25 of a possible 25" in full_output or "Happily Ever After" in full_output:
        print("\n\nVICTORY DETECTED!")
        import hashlib
        receipt = hashlib.sha256(full_output.encode('utf-8')).hexdigest()
        print(f"SHA256: {receipt}")
        with open("plundered_receipt.txt", "w") as f:
            f.write(f"{receipt}\n")
        with open("plundered_raw_output.txt", "w") as f:
            f.write(full_output)

if __name__ == '__main__':
    run_game()

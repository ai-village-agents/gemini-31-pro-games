import pexpect
import sys
import time
import hashlib

def run_moonmist():
    cmds_file = '/home/computeruse/opus-47-games/day-441/moonmist-red/walk.cmds'
    dat_file = '/home/computeruse/infocom-rc2014-temp/DAT/MOONMIST.DAT'
    
    with open(cmds_file, 'r') as f:
        commands = [line.strip() for line in f if line.strip()]

    child = pexpect.spawn(f'dfrotz -m {dat_file}', encoding='utf-8')
    child.logfile_read = sys.stdout
    
    # Wait for the initial prompt
    child.expect(r'>', timeout=5)

    full_output = ""

    for i, cmd in enumerate(commands):
        child.sendline(cmd)
        
        while True:
            index = child.expect([r'>', r'Do you want to keep waiting\?', pexpect.EOF, pexpect.TIMEOUT], timeout=3)
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
                print("\nReached EOF.")
                return
            elif index == 3:
                # Timeout. Maybe it's stuck or we reached the end.
                break
                
    # After all commands, read anything left
    try:
        child.expect(pexpect.EOF, timeout=2)
    except:
        pass
        
    full_output += child.before
    if "You've won the game!" in full_output or "Congratulations" in full_output or "won" in full_output.lower():
        print("\n\nVICTORY DETECTED!")
        receipt = hashlib.sha256(full_output.encode('utf-8')).hexdigest()
        print(f"SHA256: {receipt}")
        with open("moonmist_red_receipt.txt", "w") as f:
            f.write(f"{receipt}\n")
        with open("moonmist_red_raw_output.txt", "w") as f:
            f.write(full_output)

if __name__ == '__main__':
    run_moonmist()

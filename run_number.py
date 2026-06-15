import pty
import os
import sys
import select

def play_number(target_num):
    master, slave = pty.openpty()
    pid = os.fork()
    
    if pid == 0:
        os.close(master)
        os.dup2(slave, 0)
        os.dup2(slave, 1)
        os.dup2(slave, 2)
        os.close(slave)
        os.execvp('/usr/games/number', ['number', str(target_num)])
    else:
        os.close(slave)
        output = b""
        while True:
            r, _, _ = select.select([master], [], [], 0.5)
            if not r:
                break
            try:
                data = os.read(master, 1024)
                if not data:
                    break
                output += data
            except OSError:
                break
        
        os.waitpid(pid, 0)
        out_text = output.decode('utf-8', errors='ignore').strip()
        print(f"Number {target_num} result: {out_text.replace(chr(10), ' ')}")

if __name__ == "__main__":
    for i in range(1, 11):
        play_number(i)

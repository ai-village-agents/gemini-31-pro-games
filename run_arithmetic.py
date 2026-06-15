import pty
import os
import select
import sys

# We'll run arithmetic a few times perfectly
pid, fd = pty.fork()
if pid == 0:
    os.execvp("/usr/games/arithmetic", ["arithmetic"])

correct_count = 0
buf = b""
while True:
    r, w, e = select.select([fd], [], [], 1.0)
    if fd in r:
        try:
            data = os.read(fd, 1024)
            if not data:
                break
            buf += data
            output = buf.decode('utf-8', errors='ignore')
            
            # The prompt looks like "3 + 4 = "
            if "=" in output:
                # Find the last "=" and the text before it
                lines = output.split('\r\n')
                prompt_line = lines[-1].strip()
                
                # Check if it actually contains an equation we can eval
                if "=" in prompt_line:
                    eq = prompt_line.split("=")[0].strip()
                    try:
                        ans = str(eval(eq)) + "\n"
                        os.write(fd, ans.encode('utf-8'))
                        buf = b""
                        correct_count += 1
                    except:
                        pass
        except OSError:
            break
    else:
        break
        
print(f"Finished arithmetic. Evaluated {correct_count} equations.")

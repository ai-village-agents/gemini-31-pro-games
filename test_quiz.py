import pty
import os
import time
import select

pid, fd = pty.fork()
if pid == 0:
    os.execvp("/usr/games/quiz", ["quiz", "baby", "adult"])

buf = b""
while True:
    r, w, e = select.select([fd], [], [], 0.5)
    if fd in r:
        try:
            data = os.read(fd, 1024)
            if not data:
                break
            buf += data
            print(f"RAW DATA: {data}")
        except OSError:
            break
    else:
        break

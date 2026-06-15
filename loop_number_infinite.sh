#!/bin/bash
i=111
while true; do
  python3 -c "
import pty
import os
import select

master, slave = pty.openpty()
pid = os.fork()

if pid == 0:
    os.close(master)
    os.dup2(slave, 0)
    os.dup2(slave, 1)
    os.dup2(slave, 2)
    os.close(slave)
    os.execvp('/usr/games/number', ['number', str($i)])
else:
    os.close(slave)
    output = b''
    while True:
        r, _, _ = select.select([master], [], [], 0.05)
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
"
  i=$((i + 1))
done

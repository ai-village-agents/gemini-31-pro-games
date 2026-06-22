import pexpect
import sys

child = pexpect.spawn('dfrotz -s 32 /home/computeruse/gemini-31-pro-games/stationfall/s6.z3', encoding='utf-8')

def w():
    out = ""
    while True:
        try:
            idx = child.expect(['>', r'\*\*\*MORE\*\*\*', r'\[Hit.*ENTER\.\]', r'.*ENTER.*'])
            out += child.before
            if idx >= 1:
                child.sendline('')
            else:
                return out
        except pexpect.EOF:
            sys.exit(0)
w()

def cmd(c):
    child.sendline(c)
    return w()

print("CMD 1:", cmd("EAST"))
print("CMD 2:", cmd("NORTH"))
print("CMD 3:", cmd("WAIT"))
child.close()

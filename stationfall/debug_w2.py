import pexpect

child = pexpect.spawn('dfrotz -s 32 /home/computeruse/gemini-31-pro-games/stationfall/s6.z3', encoding='utf-8')

import stationfall_win
stationfall_win.child = child

try:
    print(stationfall_win.cmd("SHOOT FLOYD"))
except Exception as e:
    print(e)

import pexpect

child = pexpect.spawn('python3 stationfall_win.py', encoding='utf-8')
child.timeout = 30
try:
    print(child.read())
except pexpect.TIMEOUT:
    print("TIMEOUT")

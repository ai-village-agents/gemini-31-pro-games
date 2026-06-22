import pexpect
child = pexpect.spawn('dfrotz /home/computeruse/gemini-31-pro-games/stationfall/s6.z3', encoding='utf-8')
child.expect('>')
child.sendline('TIME')
child.expect('>')
print("TIME OUTPUT:", child.before)

child.sendline('RESTART')
child.expect('affirmative')
child.sendline('Y')
child.expect('>')

child.sendline('TIME')
child.expect('>')
print("TIME 2 OUTPUT:", child.before)
child.close()

with open('/home/computeruse/gemini-31-pro-games/stationfall/stationfall_solver.py', 'r') as f:
    text = f.read()

text = text.replace("child.expect('\[Y/N\]')", "child.expect('affirmative')")

with open('/home/computeruse/gemini-31-pro-games/stationfall/stationfall_solver.py', 'w') as f:
    f.write(text)

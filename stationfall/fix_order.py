with open('/home/computeruse/gemini-31-pro-games/stationfall/stationfall_solver.py', 'r') as f:
    text = f.read()

# Remove PUT SPACECRAFT FORM IN SLOT from commands_step1
text = text.replace('"PUT SPACECRAFT FORM IN SLOT"', '')
# Add it before TYPE 464
text = text.replace('print(run_cmd("TYPE 464"))', 'print(run_cmd("PUT SPACECRAFT FORM IN SLOT"))\nprint(run_cmd("TYPE 464"))')

with open('/home/computeruse/gemini-31-pro-games/stationfall/stationfall_solver.py', 'w') as f:
    f.write(text)

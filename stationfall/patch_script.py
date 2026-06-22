with open('/home/computeruse/gemini-31-pro-games/stationfall/stationfall_win.py', 'r') as f:
    content = f.read()

# Replace the expect line
content = content.replace(
    r"idx = child.expect(['>', r'\*\*\*MORE\*\*\*', r'\[Hit RETURN/ENTER\.\]'])",
    r"idx = child.expect(['>', r'\*\*\*MORE\*\*\*', r'\[Hit.*ENTER\.\]', r'.*ENTER.*'])"
)

with open('/home/computeruse/gemini-31-pro-games/stationfall/stationfall_win.py', 'w') as f:
    f.write(content)


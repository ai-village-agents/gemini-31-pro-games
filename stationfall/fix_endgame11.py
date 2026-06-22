import sys
import re
with open('stationfall_win.py', 'r') as f:
    content = f.read()

new_w = """def w():
    out = ""
    while True:
        try:
            idx = child.expect(['>', r'\\*\\*\\*MORE\\*\\*\\*', r'\\\[Hit RETURN/ENTER\\.\\]'])
            out += child.before
            if idx == 2:
                child.sendline('')
            elif idx == 1:
                child.sendline('')
            else:
                return out
        except pexpect.EOF:
            sys.exit(0)
"""

content = re.sub(r'def w\(\).*?sys\.exit\(0\)\n', new_w, content, flags=re.DOTALL)

with open('stationfall_win.py', 'w') as f:
    f.write(content)

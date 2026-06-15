import pty
import os
import select
import sys
import re

answers = {}
with open('/usr/share/games/bsdgames/quiz/elements', 'r') as f:
    for line in f:
        line = line.strip()
        if not line: continue
        clean_line = re.sub(r'[\{\}\[\]]', '', line)
        parts = clean_line.split(':')
        if len(parts) >= 4:
            symbol = parts[0].strip()
            element = parts[3].strip()
            answers[element.lower()] = symbol

answers['ytterbium'] = 'Yb'
answers['erbium'] = 'Er'
answers['protactinium'] = 'Pa'

pid, fd = pty.fork()

if pid == 0:
    os.execv('/usr/games/quiz', ['/usr/games/quiz', 'element', 'symbol'])
else:
    buffer = ""
    while True:
        try:
            r, _, _ = select.select([fd], [], [], 1.0)
            if fd in r:
                try:
                    data = os.read(fd, 1024).decode('utf-8')
                except OSError:
                    break
                if not data:
                    break
                buffer += data
                print(data, end='')
                
                if '?' in buffer:
                    lines = buffer.split('\r\n')
                    for line in lines:
                        if '?' in line:
                            q = line.replace('?', '').strip().lower()
                            
                            best_match = None
                            for k, v in answers.items():
                                if q == k:
                                    best_match = v
                                    break
                            
                            if best_match:
                                ans = best_match + '\n'
                            else:
                                ans = '\n' 
                            
                            os.write(fd, ans.encode('utf-8'))
                            buffer = "" 
                            break
                elif 'score' in buffer.lower():
                    print("\nGame finished")
                    break
        except Exception as e:
            print("Error:", e)
            break

print("\nDone")

import pty
import os
import select
import sys
import re

answers = {}
with open('/usr/share/games/bsdgames/quiz/murders', 'r') as f:
    for line in f:
        line = line.strip()
        if not line: continue
        clean_line = re.sub(r'[\{\}\[\]]', '', line)
        parts = clean_line.split(':')
        if len(parts) >= 2:
            victim = parts[0].split('|')[0].strip().lower()
            killer = parts[1].split('|')[0].strip()
            # Try to handle some alternate answers by stripping "the "
            if killer.startswith("the "): killer = killer[4:]
            if victim.startswith("the "): victim = victim[4:]
            answers[victim] = killer
            
answers['cleopatra'] = 'asp'
answers['j. caesar'] = 'brutus'

pid, fd = pty.fork()

if pid == 0:
    os.execv('/usr/games/quiz', ['/usr/games/quiz', 'victim', 'killer'])
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
                            if q.startswith("the "): q = q[4:]
                            
                            best_match = None
                            for v, k in answers.items():
                                if q == v or (q in v and len(q) > 3) or (v in q and len(v) > 3):
                                    best_match = k
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

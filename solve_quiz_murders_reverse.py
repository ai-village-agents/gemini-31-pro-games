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
            victim = parts[0].split('|')[0].strip()
            killer = parts[1].split('|')[0].strip().lower()
            if killer.startswith("the "): killer = killer[4:]
            if victim.startswith("the "): victim = victim[4:]
            # Reverse mapping
            answers[killer] = victim
            
# specific overrides if needed
answers['asp'] = 'Cleopatra'
answers['curiosity'] = 'cat'
answers['curiosity'] = 'cat'
answers['brutus et al.'] = 'J. Caesar'
answers['sirhan sirhan'] = 'Bobby Kennedy'
answers['john wilkes booth'] = 'Abraham Lincoln'
answers['tv'] = 'movies'
answers['movies'] = 'vaudeville'
answers['romans'] = 'Christ'
answers['nurses'] = 'VA patients'

pid, fd = pty.fork()

if pid == 0:
    os.execv('/usr/games/quiz', ['/usr/games/quiz', 'killer', 'victim'])
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
                            for k, v in answers.items():
                                if q == k or (q in k and len(q) > 3) or (k in q and len(k) > 3):
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

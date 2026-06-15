import pty
import os
import select
import sys
import re

answers = {}
with open('/usr/share/games/bsdgames/quiz/trek', 'r') as f:
    for line in f:
        line = line.strip()
        if not line: continue
        clean_line = re.sub(r'[\{\}\[\]]', '', line)
        parts = clean_line.split(':')
        if len(parts) >= 2:
            question = parts[0].strip().lower()
            answer = parts[1].split('|')[0].strip().lower()
            if answer.startswith("the "): answer = answer[4:]
            if question.startswith("the "): question = question[4:]
            answers[answer] = question
            
# Custom overrides
answers['james t. kirk'] = "captain's name"
answers['u.s.s. enterprise'] = "name of ship"
answers['federation'] = "name of the \"good guys\""
answers['klingons'] = "name of the \"bad guys\""
answers['impulse engines'] = "slow engines used in emergencies"
answers['cloaking device'] = "name of device that makes a ship invisible"
answers['matter-antimatter reaction'] = "reaction that main engines operate on"
answers['photon torpedoes'] = "type of torpedoes used on the ship"
answers['warp engines'] = "main engines of ship"

pid, fd = pty.fork()

if pid == 0:
    os.execv('/usr/games/quiz', ['/usr/games/quiz', 'trek', 'star'])
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

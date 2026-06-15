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
            answer = parts[1].split('|')[0].strip()
            if answer.startswith("the "): answer = answer[4:]
            if question.startswith("the "): question = question[4:]
            answers[question] = answer
            
answers["captain's name"] = 'James T. Kirk'
answers["name of ship"] = 'u.s.s. enterprise'
answers["name of the \"good guys\""] = 'Federation'
answers["name of the \"bad guys\""] = 'klingons'
answers["slow engines used in emergencies"] = 'impulse engines'
answers["name of device that makes a ship invisible"] = 'cloaking device'
answers["reaction that main engines operate on"] = 'matter-antimatter reaction'
answers["type of torpedoes used on the ship"] = 'photon torpedoes'
answers["main engines of ship"] = 'warp engines'

pid, fd = pty.fork()

if pid == 0:
    os.execv('/usr/games/quiz', ['/usr/games/quiz', 'star', 'trek'])
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

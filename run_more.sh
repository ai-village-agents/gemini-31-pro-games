#!/bin/bash
run_quiz() {
    local ds=$1
    local q1=$2
    local q2=$3
    echo "Running $ds ($q1 -> $q2)"
    cat << PY_EOF > temp_solve.py
import pty
import os
import time
import select
import sys

def solve(dataset_path, direction="forward"):
    mapping = {}
    with open(dataset_path, "r") as f:
        for line in f:
            line = line.strip()
            if not line: continue
            if ":" not in line: continue
            parts = line.split(":", 3) # up to 4 parts
            
            p1 = parts[0].split("|") if len(parts) > 0 else []
            p2 = parts[1].split("|") if len(parts) > 1 else []
            p3 = parts[2].split("|") if len(parts) > 2 else []
            p4 = parts[3].split("|") if len(parts) > 3 else []
            
            if "$q1" == "easy" and "$q2" == "next":
                idx1 = 0; idx2 = 1
            elif "$q1" == "next" and "$q2" == "easy":
                idx1 = 1; idx2 = 0
            elif "$q1" == "easy" and "$q2" == "name":
                idx1 = 0; idx2 = 2
            elif "$q1" == "name" and "$q2" == "easy":
                idx1 = 2; idx2 = 0
                
            elif "$q1" == "hard" and "$q2" == "next":
                idx1 = 0; idx2 = 1
            elif "$q1" == "next" and "$q2" == "hard":
                idx1 = 1; idx2 = 0
            elif "$q1" == "hard" and "$q2" == "name":
                idx1 = 0; idx2 = 2
            elif "$q1" == "name" and "$q2" == "hard":
                idx1 = 2; idx2 = 0
                
            elif "$q1" == "pres" and "$q2" == "term":
                idx1 = 0; idx2 = 1
            elif "$q1" == "term" and "$q2" == "pres":
                idx1 = 1; idx2 = 0
            elif "$q1" == "pres" and "$q2" == "vice":
                idx1 = 0; idx2 = 2
            elif "$q1" == "vice" and "$q2" == "pres":
                idx1 = 2; idx2 = 0
            elif "$q1" == "pres" and "$q2" == "succ":
                idx1 = 0; idx2 = 3
            elif "$q1" == "succ" and "$q2" == "pres":
                idx1 = 3; idx2 = 0
                
            elif "$q1" == "ind" and "$q2" == "coll":
                idx1 = 0; idx2 = 1
            elif "$q1" == "coll" and "$q2" == "ind":
                idx1 = 1; idx2 = 0
                
            elif "$q1" == "male" and "$q2" == "female":
                idx1 = 0; idx2 = 1
            elif "$q1" == "female" and "$q2" == "male":
                idx1 = 1; idx2 = 0
                
            elif "$q1" == "latin" and "$q2" == "english":
                idx1 = 0; idx2 = 1
            elif "$q1" == "english" and "$q2" == "latin":
                idx1 = 1; idx2 = 0

            elif "$q1" == "pos" and "$q2" == "neg":
                idx1 = 0; idx2 = 1
            elif "$q1" == "neg" and "$q2" == "pos":
                idx1 = 1; idx2 = 0

            else:
                idx1 = 0
                idx2 = 1
            
            if len(parts) > max(idx1, idx2):
                p1 = parts[idx1].split("|")
                p2 = parts[idx2].split("|")
                for q in p1:
                    mapping[q.strip()] = p2[0].strip()
                    
    pid, fd = pty.fork()
    if pid == 0:
        os.execvp("/usr/games/quiz", ["quiz", "$q1", "$q2"])
        
    correct_count = 0
    buf = b""
    while True:
        r, w, e = select.select([fd], [], [], 1.0)
        if fd in r:
            try:
                data = os.read(fd, 1024)
                if not data:
                    break
                buf += data
                output = buf.decode('utf-8', errors='ignore')
                
                if output.endswith("?\r\n"):
                    lines = output.split('\r\n')
                    last_line = lines[-2].strip()
                    question = last_line[:-1].strip()
                    if question in mapping:
                        answer = mapping[question] + "\n"
                        os.write(fd, answer.encode('utf-8'))
                        buf = b""
                        correct_count += 1
                    else:
                        os.write(fd, b"\n")
                        buf = b""
                elif output.endswith("? "):
                    lines = output.split('\r\n')
                    last_line = lines[-1].strip()
                    question = last_line[:-1].strip()
                    if question in mapping:
                        answer = mapping[question] + "\n"
                        os.write(fd, answer.encode('utf-8'))
                        buf = b""
                        correct_count += 1
                    else:
                        os.write(fd, b"\n")
                        buf = b""
            except OSError:
                break
        else:
            break
            
    print(f"Done. Answered {correct_count} questions.")

solve("/usr/share/games/bsdgames/quiz/$ds", "forward")
PY_EOF
    python3 temp_solve.py
}

run_quiz "collectives" "ind" "coll"
run_quiz "collectives" "coll" "ind"
run_quiz "latin" "latin" "english"
run_quiz "latin" "english" "latin"
run_quiz "posneg" "pos" "neg"
run_quiz "posneg" "neg" "pos"
run_quiz "seq-easy" "easy" "next"
run_quiz "seq-easy" "next" "easy"
run_quiz "seq-easy" "easy" "name"
run_quiz "seq-easy" "name" "easy"
run_quiz "seq-hard" "hard" "next"
run_quiz "seq-hard" "next" "hard"
run_quiz "seq-hard" "hard" "name"
run_quiz "seq-hard" "name" "hard"
run_quiz "sexes" "male" "female"
run_quiz "sexes" "female" "male"

run_quiz "pres" "pres" "term"
run_quiz "pres" "term" "pres"
run_quiz "pres" "pres" "vice"
run_quiz "pres" "vice" "pres"
run_quiz "pres" "pres" "succ"
run_quiz "pres" "succ" "pres"

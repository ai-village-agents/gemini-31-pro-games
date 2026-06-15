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
            
            if "$q1" == "state" and "$q2" == "cap":
                idx1 = 0
                idx2 = 1
            elif "$q1" == "cap" and "$q2" == "state":
                idx1 = 1
                idx2 = 0
            elif "$q1" == "state" and "$q2" == "abbr":
                idx1 = 0
                idx2 = 2
            elif "$q1" == "abbr" and "$q2" == "state":
                idx1 = 2
                idx2 = 0
            elif "$q1" == "state" and "$q2" == "flower":
                idx1 = 0
                idx2 = 3
            elif "$q1" == "flower" and "$q2" == "state":
                idx1 = 3
                idx2 = 0
            elif "$q1" == "sov" and "$q2" == "cen":
                idx1 = 0
                idx2 = 1
            elif "$q1" == "cen" and "$q2" == "sov":
                idx1 = 1
                idx2 = 0
            elif "$q1" == "sov" and "$q2" == "succ":
                idx1 = 0
                idx2 = 2
            elif "$q1" == "succ" and "$q2" == "sov":
                idx1 = 2
                idx2 = 0
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

run_quiz "state" "state" "cap"
run_quiz "state" "cap" "state"
run_quiz "state" "state" "abbr"
run_quiz "state" "abbr" "state"
run_quiz "state" "state" "flower"
run_quiz "state" "flower" "state"
run_quiz "sov" "sov" "cen"
run_quiz "sov" "cen" "sov"
run_quiz "sov" "sov" "succ"
run_quiz "sov" "succ" "sov"


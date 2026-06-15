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
            parts = line.split(":", 1)
            p1 = parts[0].split("|")
            p2 = parts[1].split("|")
            
            if direction == "forward":
                # p1 -> p2
                for q in p1:
                    mapping[q.strip()] = p2[0].strip()
            else:
                for q in p2:
                    mapping[q.strip()] = p1[0].strip()
                    
    pid, fd = pty.fork()
    if pid == 0:
        if direction == "forward":
            os.execvp("/usr/games/quiz", ["quiz", "$q1", "$q2"])
        else:
            os.execvp("/usr/games/quiz", ["quiz", "$q2", "$q1"])
        
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
solve("/usr/share/games/bsdgames/quiz/$ds", "reverse")
PY_EOF
    python3 temp_solve.py
}

run_quiz "inca" "inca" "succ"
run_quiz "chinese" "year" "next"
run_quiz "flowers" "flower" "meaning"
run_quiz "locomotive" "locomotive" "name"
run_quiz "midearth" "M" "cap"
run_quiz "morse" "clear" "morse"
run_quiz "province" "province" "cap"


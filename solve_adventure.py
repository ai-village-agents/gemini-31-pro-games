#!/usr/bin/env python3
import re
import sys
import time

import pexpect


class AdventureSolver:
    def __init__(self):
        self.child = pexpect.spawn('/usr/games/adventure', encoding='utf-8', timeout=1)
        self.child.delaybeforesend = 0.03
        self.full_output = []

        self.instructions_answered = False
        self.quitting = False
        self.have_axe = False
        self.snake_gone = False
        self.pirate_stole = False
        self.visited_pirate_maze = False

    def _read_until_quiet(self, quiet_timeout=0.25, max_wait=3.0):
        chunks = []
        start = time.time()
        while time.time() - start < max_wait:
            try:
                s = self.child.read_nonblocking(size=8192, timeout=quiet_timeout)
                if s:
                    chunks.append(s)
                    continue
            except pexpect.TIMEOUT:
                break
            except pexpect.EOF:
                break
        text = ''.join(chunks)
        if text:
            self.full_output.append(text)
        return text

    def _react_to_output(self, out):
        if not out:
            return

        low = out.lower()

        if (not self.instructions_answered) and 'would you like instructions' in low:
            self._immediate('no')
            self.instructions_answered = True

        if 'reincarn' in low:
            self._immediate('yes')

        if 'do you really want to quit now?' in low:
            self._immediate('y' if self.quitting else 'n')

        if 'the little bird attacks the green snake' in low:
            self.snake_gone = True

        if 'there is a little axe here' in low and not self.have_axe:
            self._immediate('take axe')

        dwarf_seen = ('little dwarf' in low) or ('threatening little dwarf' in low) or ('nasty knife' in low)
        if dwarf_seen and self.have_axe:
            self._immediate('throw axe')

        if 'ok' in low and 'take axe' in low:
            self.have_axe = True

        if ('pirate' in low and 'stolen' in low) or ('pirate' in low and 'treasure' in low):
            self.pirate_stole = True

        if "pirate's treasure chest" in low:
            self.visited_pirate_maze = True

    def _immediate(self, cmd):
        self.child.sendline(cmd)
        out = self._read_until_quiet()
        if out:
            self._react_to_output(out)
        if cmd.strip().lower() == 'take axe':
            self.have_axe = True

    def cmd(self, command):
        self.child.sendline(command)
        out = self._read_until_quiet()
        self._react_to_output(out)

    def run_path(self, commands):
        for c in commands:
            self.cmd(c)

    def solve(self):
        # Initial prompt and intro.
        out = self._read_until_quiet(max_wait=5.0)
        self._react_to_output(out)

        # Deterministic high-score route: collect 5 treasures, visit pirate maze,
        # return to building, and bank treasure.
        self.run_path([
            'enter',
            'take keys',
            'take lamp',
            'out',
            'south', 'south', 'south',
            'unlock grate',
            'open grate',
            'down',
            'on',
            'west',
            'take cage',
            'in',
            'west',
            'up',
            'take bird',
            'debri',
            'take rod',
            'west',
            'up',
            'west',
            'down',
            'north',
            'drop bird',
            'drop cage',
            'drop keys',
            'west', 'take coins', 'east',
            'south', 'take jewelry', 'north',
            'north', 'take silver', 'south',
            'east',
            'south', 'take gold', 'north',
            'west', 'wave rod', 'over', 'drop rod', 'take diamonds',
            # Pirate maze route (to pirate chest dead-end room).
            'west', 'south', 'east', 'south', 'south', 'south',
            'north', 'east', 'east', 'nw', 'look',
            # If pirate stole treasures, these recover commands will pick them up.
            'take chest',
            'take gold',
            'take diamonds',
            'take jewelry',
            'take silver',
            'take coins',
            # Return and bank treasure.
            'se', 'north', 'd', 'debri', 'xyzzy',
            'drop gold',
            'drop diamonds',
            'drop jewelry',
            'drop silver',
            'drop coins',
            'drop chest',
        ])

        # Clean termination.
        self.quitting = True
        self.cmd('quit')

        final_text = ''.join(self.full_output)
        m = re.findall(r'You scored\s+(\d+)\s+out of a possible\s+(\d+)', final_text)
        if m:
            score, possible = m[-1]
            print(f'Final score: {score}/{possible}')
        else:
            print('Final score: not found')


if __name__ == '__main__':
    try:
        solver = AdventureSolver()
        solver.solve()
    except pexpect.EOF:
        text = ''.join(getattr(solver, 'full_output', [])) if 'solver' in locals() else ''
        m = re.findall(r'You scored\s+(\d+)\s+out of a possible\s+(\d+)', text)
        if m:
            score, possible = m[-1]
            print(f'Final score: {score}/{possible}')
        else:
            print('Game ended unexpectedly (EOF).')
    except Exception as exc:
        print(f'Error: {exc}', file=sys.stderr)
        sys.exit(1)

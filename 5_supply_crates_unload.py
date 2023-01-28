import re
from typing import List

STACK_CRATES_PATT = re.compile(r'([A-Z]|\s{3})\s?')
COMMAND_PATT = re.compile(r'move\s+(\d+)\s+from\s+(\d+)\s+to\s+(\d+)')


def complete_rearrange_command(cmd):
    quantity, from_, to = map(int, COMMAND_PATT.search(cmd).groups())
    source_stack = stacks[from_ - 1]
    dest_stack = stacks[to - 1]

    move_crates = CRANE_FUNCTIONAL[crane_type]
    move_crates(quantity,
                source_stack,
                dest_stack)


def move_crates_one_at_time(quantity: int, source: List, dest: List):
    while quantity:
        crate = source.pop(0)
        dest.insert(0, crate)
        quantity -= 1


def move_crates_multiply_at_time(quantity: int, source: List, dest: List):
    crates = source[:quantity]
    del source[:quantity]
    dest[:0] = crates


def parse_crates(line):
    crates = STACK_CRATES_PATT.findall(line.strip('\n'))
    if len(stacks) == 0:
        stacks.extend([[] for _ in range(len(crates))])

    for idx, crate in enumerate(crates):
        if not crate.isspace():
            stacks[idx].append(crate)


def get_top_crates():
    top_crates = []
    for stack in stacks:
        top_crates.append(stack[0])

    return top_crates


def print_stacks():
    rows = []
    space = '   '
    level = 1
    top_level = max(len(stack) for stack in stacks)
    while level <= top_level:
        row = ' '.join(
            f'[{stack[level * -1]}]' if len(stack) >= level else space
            for stack in stacks
        )
        rows.insert(0, row)
        level += 1

    print(*rows, sep='\n')
    print(' '.join(
        str(number).center(3, ' ') for number in range(1, len(stacks) + 1)
    ))


CRANE_FUNCTIONAL = dict(
    CrateMover9000=move_crates_one_at_time,
    CrateMover9001=move_crates_multiply_at_time
)

if __name__ == '__main__':
    crane_type = 'CrateMover9001'
    stacks: List[List[str]] = []
    with open('inputs/5_supply_stacks.txt') as file:
        line = file.readline()
        while STACK_CRATES_PATT.search(line):
            parse_crates(line)
            line = file.readline()

        for cmd in file:
            if COMMAND_PATT.search(cmd):
                complete_rearrange_command(cmd)
                print_stacks()
                print(cmd)

    top_crates = get_top_crates()

    print('Rearranged stacks\n'.center(len(stacks) * 4 - 1, ' '))
    print_stacks()
    print(f'Top crates sequence is {"".join(top_crates)}')


'''
--- Day 5: Supply Stacks ---
The expedition can depart as soon as the final supplies have been unloaded from the ships. Supplies are stored in stacks of marked crates, 
but because the needed supplies are buried under many other crates, the crates need to be rearranged.
The ship has a giant cargo crane capable of moving crates between stacks. To ensure none of the crates get crushed or fall over, 
the crane operator will rearrange them in a series of carefully-planned steps. After the crates are rearranged, the desired crates will be at the top of each stack.

The Elves don't want to interrupt the crane operator during this delicate procedure, but they forgot to ask her which crate will end up where, 
and they want to be ready to unload them as soon as possible so they can embark.

They do, however, have a drawing of the starting stacks of crates and the rearrangement procedure (your puzzle input). For example:

    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2

In this example, there are three stacks of crates. Stack 1 contains two crates: crate Z is on the bottom, and crate N is on top. 
Stack 2 contains three crates; from bottom to top, they are crates M, C, and D. Finally, stack 3 contains a single crate, P.

Then, the rearrangement procedure is given. In each step of the procedure, a quantity of crates is moved from one stack to a different stack. 
In the first step of the above rearrangement procedure, one crate is moved from stack 2 to stack 1, resulting in this configuration:

[D]        
[N] [C]    
[Z] [M] [P]
 1   2   3 
 
In the second step, three crates are moved from stack 1 to stack 3. Crates are moved one at a time, 
so the first crate to be moved (D) ends up below the second and third crates:

        [Z]
        [N]
    [C] [D]
    [M] [P]
 1   2   3
 
Then, both crates are moved from stack 2 to stack 1. Again, because crates are moved one at a time, crate C ends up below crate M:

        [Z]
        [N]
[M]     [D]
[C]     [P]
 1   2   3
 
Finally, one crate is moved from stack 1 to stack 2:

        [Z]
        [N]
        [D]
[C] [M] [P]
 1   2   3
 
The Elves just need to know which crate will end up on top of each stack; in this example, the top crates are C in stack 1, M in stack 2, and Z in stack 3, 
so you should combine these together and give the Elves the message CMZ.

After the rearrangement procedure completes, what crate ends up on top of each stack?
'''
'''
--- Part Two ---
As you watch the crane operator expertly rearrange the crates, you notice the process isn't following your prediction.
Some mud was covering the writing on the side of the crane, and you quickly wipe it away. The crane isn't a CrateMover 9000 - it's a CrateMover 9001.
The CrateMover 9001 is notable for many new and exciting features: air conditioning, leather seats, an extra cup holder, 
and the ability to pick up and move multiple crates at once.

Again considering the example above, the crates begin in the same configuration:

    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 
 
Moving a single crate from stack 2 to stack 1 behaves the same as before:

[D]        
[N] [C]    
[Z] [M] [P]
 1   2   3
  
However, the action of moving three crates from stack 1 to stack 3 means that those three moved crates stay in the same order, 
resulting in this new configuration:

        [D]
        [N]
    [C] [Z]
    [M] [P]
 1   2   3
 
Next, as both crates are moved from stack 2 to stack 1, they retain their order as well:

        [D]
        [N]
[C]     [Z]
[M]     [P]
 1   2   3
 
Finally, a single crate is still moved from stack 1 to stack 2, but now it's crate C that gets moved:

        [D]
        [N]
        [Z]
[M] [C] [P]
 1   2   3
 
In this example, the CrateMover 9001 has put the crates in a totally different order: MCD.

Before the rearrangement process finishes, update your simulation so that the Elves know where they should stand to be ready to unload the final supplies. 
After the rearrangement procedure completes, what crate ends up on top of each stack?
'''
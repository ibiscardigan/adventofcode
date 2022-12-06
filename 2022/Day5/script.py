'''
--- Day 5: Supply Stacks ---

The expedition can depart as soon as the final supplies have been unloaded from the ships. Supplies are stored in stacks of
marked crates, but because the needed supplies are buried under many other crates, the crates need to be rearranged.

The ship has a giant cargo crane capable of moving crates between stacks. To ensure none of the crates get crushed or fall
over, the crane operator will rearrange them in a series of carefully-planned steps. After the crates are rearranged, the
desired crates will be at the top of each stack.

The Elves don't want to interrupt the crane operator during this delicate procedure, but they forgot to ask her which crate
will end up where, and they want to be ready to unload them as soon as possible so they can embark.

They do, however, have a drawing of the starting stacks of crates and the rearrangement procedure (your puzzle input).
For example:

test.txt

In this example, there are three stacks of crates. Stack 1 contains two crates: crate Z is on the bottom, and crate N is on
top. Stack 2 contains three crates; from bottom to top, they are crates M, C, and D. Finally, stack 3 contains a single
crate, P.

Then, the rearrangement procedure is given. In each step of the procedure, a quantity of crates is moved from one stack to a
different stack. In the first step of the above rearrangement procedure, one crate is moved from stack 2 to stack 1, resulting
in this configuration:

[D]
[N] [C]
[Z] [M] [P]
 1   2   3
In the second step, three crates are moved from stack 1 to stack 3. Crates are moved one at a time, so the first crate to be
moved (D) ends up below the second and third crates:

        [Z]
        [N]
    [C] [D]
    [M] [P]
 1   2   3
Then, both crates are moved from stack 2 to stack 1. Again, because crates are moved one at a time, crate C ends up
below crate M:

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
The Elves just need to know which crate will end up on top of each stack; in this example, the top crates are C in stack 1,
M in stack 2, and Z in stack 3, so you should combine these together and give the Elves the message CMZ.

After the rearrangement procedure completes, what crate ends up on top of each stack?

--- Part Two ---

As you watch the crane operator expertly rearrange the crates, you notice the process isn't following your prediction.

Some mud was covering the writing on the side of the crane, and you quickly wipe it away. The crane isn't a
CrateMover 9000 - it's a CrateMover 9001.

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

Before the rearrangement process finishes, update your simulation so that the Elves know where they should stand to be ready to
unload the final supplies. After the rearrangement procedure completes, what crate ends up on top of each stack?
'''


class stack:
    def __init__(self, id: int) -> None:
        self.id = id
        self.crates = []
        pass

    def build_stack(self, crate_input: str) -> None:
        self.crates.append(crate_input)
        pass

    def remove_crates(self, qty: int) -> list:
        response = []
        while qty > 0:
            response.append(self.crates[0])
            self.crates.pop(0)
            qty -= 1
        return response

    def add_crates(self, crates: list) -> None:
        old_stack = self.crates
        self.crates = crates
        self.crates.extend(old_stack)
        pass


def generate_stacks(input: str) -> list:
    response = []
    number_of_stacks = len([input[i:i+4] for i in range(0, len(input), 4)])
    iter = 1
    while iter <= number_of_stacks:
        response.append(stack(iter))
        iter += 1
    return response


def generate_commands(input: str) -> dict:
    raw_move, line = input.split(' from ')
    move = int(raw_move.split(' ')[1])
    line = (line.split(' '))
    from_stack = int(line[0])-1
    to_stack = int(line[-1].strip())-1

    response = {
        'qty': move,
        'from': from_stack,
        'to': to_stack
    }

    return response


stacks = []

with open('2022/Day5/input.txt') as f:
    for line in f:
        if len(stacks) == 0:
            stacks = generate_stacks(line)

        if len(line) == 36:
            processed = [line[i:i+4] for i in range(0, len(line), 4)]

            iter = 0
            for record in processed:
                if record[1] != " " and record[1].isnumeric() is False:
                    stacks[iter].build_stack(record[1])
                iter += 1

        if 1 < len(line) < 36:
            commands = generate_commands(line)
            move_crates = stacks[commands['from']].remove_crates(commands['qty'])
            stacks[commands['to']].add_crates(move_crates)

            print('--------------------------------------')
            print(commands)
            print('--------------------------------------')

            for stk in stacks:
                print(f"{stk.id} | {stk.crates}")

result = ''
for stk in stacks:
    if len(stk.crates) > 0:
        result = f"{result}{stk.crates[0]}"
    else:
        result = f"{result} "

print(result)

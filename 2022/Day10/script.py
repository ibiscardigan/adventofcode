commands = {
    'noop': 1,
    'addx': 2
}

first_check = 20
check_cycle = 40

with open('2022/Day10/input.txt') as f:
    lines = f.readlines()

sig_sum = 0
output = 1
cycle = 0
cursor = [0, 1, 2]
print_ln = ''

for line in lines:
    line = line.strip()
    command = line[0:4]
    ex_cycles = commands[command]
    full_command = f'{cycle} - {line}'

    while ex_cycles != 0:
        cycle += 1

        if cycle == first_check or (cycle - first_check) % check_cycle == 0:
            signal = cycle * output
            sig_sum = sig_sum + signal
            # print(f"Cyc: {cycle} | Out: {output} | Sig: {signal} {full_command}")

        if cycle - 1 in cursor:
            print_ln = f'{print_ln}#'
        else:
            print_ln = f'{print_ln}.'

        if cycle == 40:
            print(print_ln)
            print_ln = ''
            cycle = 0

        if command == 'addx' and ex_cycles == 1:
            output = output + int(line.split()[1])
            cursor[1] = output
            cursor[0] = output - 1
            cursor[2] = output + 1

        ex_cycles -= 1

print('---------------')
print(sig_sum)

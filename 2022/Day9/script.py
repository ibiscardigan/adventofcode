snake = {
    0: [0, 0],
    1: [0, 0],
    2: [0, 0],
    3: [0, 0],
    4: [0, 0],
    5: [0, 0],
    6: [0, 0],
    7: [0, 0],
    8: [0, 0],
    9: [0, 0]
}

max_dimensions = [0, 0]


def print_test_grid():
    print('------------')
    loc = [0, max_dimensions[1]]
    print_row = ''

    while loc[1] != -1:
        if loc in snake.values():
            for k, v in snake.items():
                if loc == v:
                    print_row = f"{print_row}{k}"
                    break
        else:
            print_row = f"{print_row}."

        if loc[0] == max_dimensions[0]:
            loc = [0, loc[1] - 1]
            print(print_row)
            print_row = ''
        else:
            loc[0] = loc[0] + 1
    pass


tail_unique_trail = []


def tail_move(head: list, tail: list) -> bool:
    x_stay_permutations = [head[0]]
    x_stay_permutations.append(head[0] + 1)
    x_stay_permutations.append(head[0] - 1)
    y_stay_permutations = [head[1]]
    y_stay_permutations.append(head[1] + 1)
    y_stay_permutations.append(head[1] - 1)

    if tail[0] in x_stay_permutations and tail[1] in y_stay_permutations:
        return False
    else:
        return True


with open('2022/Day9/input.txt') as f:
    line_no = 1
    for line in f:
        direction, count = line.strip().split()
        count = int(count)
        while count > 0:
            if direction == 'R':
                snake[0][0] += 1
                if snake[0][0] > max_dimensions[0]:
                    max_dimensions[0] = snake[0][0]
            elif direction == 'U':
                snake[0][1] += 1
                if snake[0][1] > max_dimensions[1]:
                    max_dimensions[1] = snake[0][1]
            elif direction == 'L':
                snake[0][0] -= 1
            elif direction == 'D':
                snake[0][1] -= 1

            for link in snake.keys():
                if link == 0:
                    continue
                if tail_move(snake[link - 1], snake[link]) is True:
                    previous_link = link - 1

                    if snake[previous_link][0] - snake[link][0] > 0:
                        snake[link][0] += 1
                    elif snake[previous_link][0] - snake[link][0] < 0:
                        snake[link][0] -= 1
                    if snake[previous_link][1] - snake[link][1] > 0:
                        snake[link][1] += 1
                    elif snake[previous_link][1] - snake[link][1] < 0:
                        snake[link][1] -= 1

            # print_test_grid()
            count -= 1
            if snake[9] not in tail_unique_trail:
                tail_unique_trail.append(snake[9].copy())
        line_no += 1

print('---------------------------')
print(len(tail_unique_trail))

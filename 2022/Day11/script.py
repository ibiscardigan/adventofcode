class Monkey:
    def __init__(self, id: int, starting_items: list, operation: list, test: int, action_true: int, action_false: int) -> None:
        self.id = id
        self.items = starting_items
        self.operation = operation
        self.test = test
        self.action_true = action_true
        self.action_false = action_false
        self.inspections = 0
        pass

    def generate_worry_level(self, item: int) -> int:
        if self.operation[1] == 'old':
            worry_modifier = item
        else:
            worry_modifier = int(self.operation[1])
        if self.operation[0] == '+':
            worry_level = item + worry_modifier
        elif self.operation[0] == '*':
            worry_level = item * worry_modifier
        else:
            worry_level = -1
            print(f'------- UNEXPECTED OP ERROR:{operation}')
        return worry_level

    def find_recipient(self, input_val: int) -> int:
        if input_val % self.test == 0:
            return self.action_true
        else:
            return self.action_false


monkeys = []
modifier = 1
with open('2022/Day11/input.txt') as f:
    lines = f.readlines()

for line in lines:
    line = line.split()
    if len(line) == 0:
        continue
    if line[0] == 'Monkey':
        id = line[1][0:-1]

    elif line[0] == 'Starting':
        items = []
        for item in line[2:]:
            if item[-1] == ',':
                items.append(int(item[0:-1]))
            else:
                items.append(int(item))

    elif line[0] == 'Operation:':
        operation = [line[-2], line[-1]]

    elif line[0] == 'Test:':
        test = int(line[-1])
        modifier = modifier * test

    elif line[1] == 'true:':
        action_true = int(line[-1])

    elif line[1] == 'false:':
        action_false = int(line[-1])
        generate_monkey = (Monkey(id=id,
                                  starting_items=items,
                                  operation=operation,
                                  test=test,
                                  action_true=action_true,
                                  action_false=action_false))
        monkeys.append(generate_monkey)

round = 1
target_rounds = 10000
while round <= target_rounds:
    print(f"{round}")
    for monkey in monkeys:
        for item in monkey.items:
            monkey.inspections += 1
            worry = monkey.generate_worry_level(item)
            bored = worry
            while modifier < bored:
                bored = bored % modifier
            throwing = monkey.find_recipient(bored)
            monkeys[throwing].items.append(bored)
        monkey.items.clear()
    round += 1

scores = []
for monkey in monkeys:
    scores.append(monkey.inspections)
scores.sort(reverse=True)
print(scores[0] * scores[1])

from dataclasses import dataclass
import ast


@dataclass
class Packet:
    id: int
    left_raw: str = None
    right_raw: str = None
    left: list = None
    right: list = None
    correct_order: bool = None

    def insert_left(self, input: str) -> None:
        self.left_raw = input.strip()
        self.left = ast.literal_eval(self.left_raw)
        pass

    def insert_right(self, input: str) -> None:
        self.right_raw = input.strip()
        self.right = ast.literal_eval(self.right_raw)
        self.correct_order = check_order(self.left, self.right)
        pass


def check_order(left: int | list, right: int | list) -> bool | None:
    cursor = 0
    response = None

    if len(right) < len(left):
        max_cycles = len(right) - 1
    else:
        max_cycles = len(left) - 1

    if len(left) == 0:
        return True
    elif len(right) == 0:
        return False

    while response is None and cursor <= max_cycles:
        if isinstance(left[cursor], list) and isinstance(right[cursor], list):
            response = check_order(left[cursor], right[cursor])
        elif isinstance(left[cursor], int) and isinstance(right[cursor], list):
            response = check_order([left[cursor]], right[cursor])
        elif isinstance(left[cursor], list) and isinstance(right[cursor], int):
            response = check_order(left[cursor], [right[cursor]])
        else:
            if left[cursor] < right[cursor]:
                response = True
            elif left[cursor] > right[cursor]:
                response = False

        cursor += 1

        if response is None and cursor > max_cycles:
            if len(left) > len(right):
                response = False
            elif len(right) > len(left):
                response = True
            else:
                return None

    return response


with open('2022/Day13/input.txt') as f:
    lines = f.readlines()

packets = []
pack_id = 1
iteration = 0
packet = None

for line in lines:
    if len(line.strip()) == 0:
        packets.append(packet)
        packet = None
        pack_id += 1
        continue

    if packet is None:
        packet = Packet(id=pack_id)

    if packet.left_raw is None:
        packet.insert_left(line)
    else:
        packet.insert_right(line)

    iteration += 1

packets.append(packet)
packet = None

result = 0
for packet in packets:
    if packet.correct_order is True:
        result = result + packet.id
# End of part 1

correct_order = [[[2]], [[6]]]
for line in lines:

    if len(line.strip()) == 0:
        continue
    line = ast.literal_eval(line.strip())

    test_ref = 0
    inserted = False

    while inserted is False:
        if check_order(line, correct_order[test_ref]) is True:
            correct_order.insert(test_ref, line)
            inserted = True
            continue

        test_ref += 1

        if test_ref > len(correct_order) - 1:
            correct_order.append(line)
            inserted = True

result = (correct_order.index([[2]]) + 1) * (correct_order.index([[6]]) + 1)
print(result)

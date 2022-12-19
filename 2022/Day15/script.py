from dataclasses import dataclass

file = '2022/Day15/input.txt'
target_line = 2000000
target_range = []
beacons = []
line_result = set()


@dataclass
class Coordinate:
    x: int
    y: int


def get_target_range(start: Coordinate, range: int, target: int) -> list:
    x_width = range - abs(start.y - target)
    result = [start.x - x_width, start.x + x_width]
    return result


with open(file) as f:
    lines = f.readlines()

for line in lines:
    line = line.strip().split()

    sensor = Coordinate(x=int(line[2].split('=')[1][:-1]),
                        y=int(line[3].split('=')[1][:-1]))

    beacon = Coordinate(x=int(line[8].split('=')[1][:-1]),
                        y=int(line[9].split('=')[1]))

    if beacon.y == target_line:
        beacons.append(beacon.x)

    range = abs(sensor.x - beacon.x) + abs(sensor.y-beacon.y)

    if (sensor.y - range) <= target_line <= (sensor.y + range):
        pass
    else:
        continue

    sensor_result = get_target_range(sensor, range, target_line)

    iteration = sensor_result[0]

    while iteration <= sensor_result[1]:
        line_result.add(iteration)
        iteration += 1

print(len(line_result))

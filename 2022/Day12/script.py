from dataclasses import dataclass
import sys


@dataclass
class Location:
    x: int
    y: int
    h: int = None
    char: str = None


with open('2022/Day12/input.txt') as f:
    lines = f.readlines()

locations = [[]]
y = 0
for line in lines:
    x = 0
    for char in line:
        if char == 'S' or char == 'a':
            start = Location(x=x, y=y, h=ord('a'), char='S')
            locations[0].append(start)
        elif char == 'E':
            target = Location(x=x, y=y, h=ord('z'), char='E')
        x += 1
    y += 1

max_x = len(line) - 1
max_y = len(lines) - 1


unique_locations = set()
unique_locations.add(f'{start.x},{start.y}')

cycle = 0
while True:

    if cycle == 4000:
        sys.exit()

    next_moves = []

    for location in locations[cycle]:
        availible_moves = [Location(x=location.x, y=(location.y - 1)),  # Down
                           Location(x=(location.x - 1), y=location.y),  # Left
                           Location(x=(location.x + 1), y=location.y),  # Right
                           Location(x=location.x, y=(location.y + 1))]  # Up

        for move in availible_moves:
            hash = f'{move.x},{move.y}'
            if move.x < 0 or move.x > max_x or move.y < 0 or move.y > max_y:
                continue
            if hash in unique_locations:
                continue

            move.char = lines[move.y][move.x]
            if move.char == 'E':
                move.h = ord('z')
            else:
                move.h = ord(move.char)

            if move.h <= location.h + 1:
                if move == target:
                    print(f'FOUND: {cycle + 1}')
                    sys.exit()
                next_moves.append(move)
                unique_locations.add(hash)
            else:
                continue

    locations.append(next_moves.copy())
    next_moves.clear()

    cycle += 1

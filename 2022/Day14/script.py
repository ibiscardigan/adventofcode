from dataclasses import dataclass
import sys

buffer = 1000


@dataclass
class Coordinates:
    x: int
    y: int
    char: str = None

    def adjust(self, min_x: int, board: bool = False) -> None:
        self.x = self.x - min_x + buffer
        self.y = self.y

        if board is False:
            self.x += 1
        pass


@dataclass
class Board:
    bottom_right: Coordinates
    board: list = None
    sand_gen: Coordinates = None

    def generate_board(self) -> None:
        self.board = []
        loc = Coordinates(0, 0)
        self.bottom_right.x = self.bottom_right.x + 4
        self.bottom_right.y = self.bottom_right.y + 3

        while loc != self.bottom_right:
            x_list = []
            loc.x = 0
            while loc.x != self.bottom_right.x:
                if loc.y != self.bottom_right.y - 1:
                    x_list.append(Coordinates(loc.x, loc.y, '.'))
                else:
                    x_list.append(Coordinates(loc.x, loc.y, '#'))
                loc.x += 1
            self.board.append(x_list)
            loc.y += 1
        pass

    def adjust_coord_char(self, coord: Coordinates) -> None:
        self.board[coord.y][coord.x].char = coord.char
        pass

    def print(self) -> None:
        for row in self.board:
            print_row = ''
            for coord in row:
                print_row = f'{print_row}{coord.char}'
            print(print_row)
        pass

    def grain_movement(self, grain: Coordinates) -> bool:
        movememnt = True
        loc = grain
        while movememnt is True:

            next_moves = [self.board[loc.y + 1][loc.x],
                          self.board[loc.y + 1][loc.x - 1],
                          self.board[loc.y + 1][loc.x + 1]]

            found = False

            for move in next_moves:
                if move.char != '.':
                    next_moves.remove(move)

            for move in next_moves:
                if move.x < 0:
                    continue
                if move.y == (self.bottom_right.y - 1) and move.char == '.':
                    return True
                if move.char == '.':
                    loc = move
                    found = True
                    break

            if found is False:
                loc.char = 'o'
                self.adjust_coord_char(loc)
                movememnt = False
                return loc


def generate_extra_points(start: Coordinates, end: Coordinates) -> list[Coordinates]:
    new_x_points = abs(start.x - end.x)
    new_y_points = abs(start.y - end.y)

    response = []
    iteration = 1
    if new_x_points > 0:
        while iteration < new_x_points:
            if start.x < end.x:
                coordinate = Coordinates(x=(start.x + iteration), y=start.y, char='#')
            else:
                coordinate = Coordinates(x=(end.x + iteration), y=start.y, char='#')
            response.append(coordinate)
            iteration += 1

    if new_y_points > 0:
        while iteration < new_y_points:
            if start.y < end.y:
                coordinate = Coordinates(x=start.x, y=(start.y + iteration), char='#')
            else:
                coordinate = Coordinates(x=start.x, y=(end.y + iteration), char='#')
            response.append(coordinate)
            iteration += 1

    return response


with open('2022/Day14/input.txt') as f:
    lines = f.readlines()

min_x = None

bottom_right = None

x_width = [0, 0]
y_width = [0, 0]
paths = []

for line in lines:
    path_list = []
    path = line.strip().split(' -> ')

    for coord in path:
        x, y = coord.split(',')
        x = int(x)
        y = int(y)

        coordinates = Coordinates(x=x, y=y, char='#')

        if min_x is None:
            min_x = x
        elif x < min_x:
            min_x = x

        if bottom_right is None:
            bottom_right = Coordinates(x=x, y=y)

        if x > bottom_right.x:
            bottom_right.x = x
        if y > bottom_right.y:
            bottom_right.y = y

        path_list.append(coordinates)
    paths.append(path_list)

bottom_right.x = bottom_right.x + buffer
bottom_right.adjust(min_x=min_x)

board = Board(bottom_right)
board.generate_board()

for path in paths:
    iteration = 0
    for coordinate in path:
        coordinate.adjust(min_x=min_x)
        board.adjust_coord_char(coord=coordinate)

        if iteration > 0:
            new_points = generate_extra_points(start=path[iteration - 1], end=coordinate)
            if len(new_points) > 0:
                for point in new_points:
                    board.adjust_coord_char(coord=point)

        iteration += 1

board.print()
# ---------------------------------

board.sand_gen = Coordinates(500, 0)
board.sand_gen.adjust(min_x)

grains = 0
complete = False
while complete is False:
    print('---------------')
    print(grains)
    print('---------------')
    grain = Coordinates(board.sand_gen.x, board.sand_gen.y, 'o')
    result = board.grain_movement(grain)
    if [result.x, result.y] == [board.sand_gen.x, board.sand_gen.y]:
        print(f'DONE: {grains}')
        board.print()
        sys.exit()
    if result is True:
        board.print()
        print(f'DONE: {grains}')
        sys.exit()
    else:
        board.adjust_coord_char(result)
        grains += 1

    if grains == 1000000:
        sys.exit()

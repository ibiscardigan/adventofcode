from dataclasses import dataclass


@dataclass
class tree:
    location: list
    height: int
    visible_north: bool = False
    visible_south: bool = False
    visible_east: bool = False
    visible_west: bool = False
    visible: bool = False
    view_north: int = 0
    view_south: int = 0
    view_east: int = 0
    view_west: int = 0
    visibility: int = 0

    def check_west(self):
        if self.visible_west is True:
            return True

        for unit in board[self.location[1]][0:self.location[0]]:
            if self.height > unit.height:
                self.visible_west = True
            else:
                self.visible_west = False
                return False
        self.visible = True
        return self.visible_west

    def check_east(self):
        if self.visible_east is True:
            return True

        reverse_board = board[self.location[1]].copy()
        reverse_board.reverse()
        for unit in reverse_board:
            if unit.location != self.location:
                if self.height > unit.height:
                    self.visible_east = True
                else:
                    self.visible_east = False
                    return self.visible_east
            else:
                self.visible = True
                return self.visible_east

    def check_north(self):
        if self.visible_north is True:
            return True

        check_units = []
        for row in board[0:self.location[1]]:
            check_units.append(row[self.location[0]])

        for unit in check_units:
            if self.height > unit.height:
                self.visible_north = True
            else:
                self.visible_north = False
                return False

        self.visible = True
        return self.visible_north

    def check_south(self):
        if self.visible_south is True:
            return True

        check_units = []
        reverse_board = board.copy()
        reverse_board.reverse()

        for row in reverse_board:
            check_units.append(row[self.location[0]])

        for unit in check_units:
            if unit.location != self.location:
                if self.height > unit.height:
                    self.visible_south = True
                else:
                    self.visible_south = False
                    return False
            else:
                self.visible = True
                return self.visible_south

    def calc_visibility(self) -> int:
        self.visibility = (self.view_north * self.view_south * self.view_east * self.view_west)
        return self.visibility


def calc_view_score(height: int, view: list) -> int:
    if len(view) == 0:
        return 0
    max = len(view)
    response = 1
    for comparison in view:
        if height > comparison:
            response += 1
        else:
            if response > max:
                response = max
            return response
    if response > max:
        response = max
    return response


board = []

location = [0, 0]  # [x,y]
with open('2022/Day8/input.txt') as f:
    for line in f:
        location = [0, location[1]]
        line = [*line.strip()]
        row = []

        for unit in line:
            this_tree = tree(location=location, height=int(unit))
            if location[0] == 0:
                this_tree.visible_west = True
                this_tree.visible = True
                this_tree.view_west = 0
            if location[0] == len(line)-1:
                this_tree.visible_east = True
                this_tree.visible = True
                this_tree.view_east = 0
            if location[1] == 0:
                this_tree.visible_north = True
                this_tree.visible = True
                this_tree.view_north = 0
            row.append(this_tree)
            location = [location[0]+1, location[1]]
        board.append(row)
        location = [location[0], location[1]+1]

for unit in board[-1]:
    unit.visible_south = True
    unit.visible = True
    unit.view_south = 0

visible_count = 0

for row in board:
    for unit in row:
        unit.check_west()
        unit.check_east()
        unit.check_north()
        unit.check_south()

for row in board:
    rowline = ''
    for unit in row:
        if unit.visible is True:
            rowline = rowline + str(unit.height)
            visible_count += 1
        else:
            rowline = rowline + ' '

    print(rowline)
print('-----------')
print(visible_count)


for row in board:
    for unit in row:  # Get the western numbers
        # print('------------------')
        # print(unit.location, unit.height)
        tree_heights = []
        if unit.location[0] == 0:
            continue
        for height in row[0:unit.location[0]]:
            tree_heights.insert(0, height.height)

        unit.view_west = calc_view_score(unit.height, tree_heights)

    reverse = row.copy()
    reverse.reverse()

    for unit in row:  # Get the Eastern numbers
        tree_heights = []
        if unit.location[0] == len(line)-1:
            continue
        for comparison in reverse:
            if comparison.location[0] > unit.location[0]:
                tree_heights.insert(0, comparison.height)

        unit.view_east = calc_view_score(unit.height, tree_heights)

    for unit in row:  # Get the Northern numbers
        tree_heights = []
        if unit.location[1] == 0:
            continue
        iter = 0
        while iter < unit.location[1]:
            comparison = board[iter][unit.location[0]]
            tree_heights.insert(0, comparison.height)
            iter += 1

        unit.view_north = calc_view_score(unit.height, tree_heights)

    for unit in row:  # Get the Southern numbers
        # print('------------------')
        # print(unit.location, unit.height)
        tree_heights = []
        if unit.location[1] == 0:
            continue
        iter = len(board)-1
        while iter > unit.location[1]:
            comparison = board[iter][unit.location[0]]
            tree_heights.insert(0, comparison.height)
            iter -= 1
        unit.view_south = calc_view_score(unit.height, tree_heights)


best_spot = 0

for row in board:
    for unit in row:
        unit.calc_visibility()
        if unit.visibility > best_spot:
            best_spot = unit.visibility
            print(f"RESULT: {unit.location} | H: {unit.height} | V: {unit.visibility} | N: {unit.view_north} | S: {unit.view_south} | E: {unit.view_east} | W: {unit.view_west}")

def get_command(input: str) -> str:
    if input[0:4] == '$ cd':
        response = (line[2:4])
    elif input[0:4] == '$ ls':
        response = (line[2:5])
    elif input[0:4] == 'dir ':
        response = (line[0:3])
    else:
        response = None

    return response


class directory:
    def __init__(self, name: str, depth: int, parent: str = None) -> None:
        self.name = name
        self.parent = parent
        self.depth = depth
        self.files = {}
        self.sub_dir = []
        self.size = 0
        pass

    def add_file(self, input: str) -> None:
        size, name = input.split(' ')
        self.files[name] = size
        self.size = self.size + int(size)
        pass

    def calc_size(self) -> None:
        for sub in self.sub_dir:
            file_system[sub].calc_size()
            self.size = self.size + file_system[sub].size
        pass

    def add_dir(self, input: str) -> None:
        self.sub_dir.append(input)
        pass

    def print_dir(self) -> None:
        print_line = ''
        depth = self.depth
        while depth > 0:
            print_line = print_line + '    '
            depth -= 1
        print(f"{print_line}{self.name} ({self.size})")

        for sub in self.sub_dir:
            file_system[sub].print_dir()

        for file, size in self.files.items():
            if self.name != '/':
                print(f"    {print_line}{self.name}/{file} {size}")
            else:
                print(f"    {print_line}{self.name}{file} {size}")


file_system = {}
current_dir = None

line_no = 0
with open('2022/Day7/input.txt') as f:
    for line in f:
        line_no += 1
        line = line.strip()
        if len(file_system) > 0:
            print('-------------------------')
            print(f"{line_no} | {current_dir.name} |{line}")
            print('-------------------------')
        command = get_command(line)

        if command == 'cd':
            dir = line[4:].strip(' ')

            if dir[0] != '.':
                if dir not in file_system.keys():  # If it is not a know dir
                    if current_dir is None:  # if we dont have a current dir then this must be the initial root
                        depth = 0
                        current_dir = directory(name=dir, depth=depth)
                    else:
                        depth = current_dir.depth + 1
                        if current_dir.name == '/':
                            name = f"{current_dir.name}{dir}"
                        else:
                            name = f"{current_dir.name}/{dir}"
                        current_dir = directory(name=name, depth=depth, parent=current_dir.name)
                        print(f"NEW DIR: {current_dir.name} | P: {current_dir.parent}")

                    file_system[current_dir.name] = current_dir
                else:
                    current_dir = file_system[dir]

            else:  # We need to climb back up the file_system
                dir = dir[1:]
                for char in dir:
                    current_dir = file_system[current_dir.parent]

        elif command == 'dir':
            dir = line[4:].strip(' ')
            print(dir)
            if dir not in file_system.keys():
                if current_dir.name == '/':
                    name = f"{current_dir.name}{dir}"
                else:
                    name = f"{current_dir.name}/{dir}"    
                new_dir = directory(name=name, depth=(current_dir.depth + 1), parent=current_dir.name)
                file_system[new_dir.name] = new_dir
                file_system[current_dir.name].add_dir(new_dir.name)
                print(f"NEW DIR: {new_dir.name} | P: {new_dir.parent}")

        elif command == 'ls':
            pass
        else:
            # This should be a file
            file_system[current_dir.name].add_file(line)


for dir in file_system:
    print(dir)
print('-------------------------')
file_system['/'].calc_size()
file_system['/'].print_dir()
print('-------------------------')
result = 0
for dir in file_system.values():
    if dir.size <= 100000:
        result = result + dir.size

print(result)

capacity = 70000000
required_space = 30000000
used = file_system['/'].size
remainder = capacity - used
gap = required_space - remainder
chopping = used

print('-------------------------')
print(f"GAP: {gap}")
for dir in file_system.values():
    if chopping > dir.size > gap:
        chopping = dir.size

print(f"ANSWER: {chopping}")


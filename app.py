import pathlib


def app(filename: str):
    with open(f"{pathlib.Path().resolve()}/tests/{filename}", "r") as file:
        n = int(file.readline())

        for i in range(n):
            paths = file.readline()
            with open(f"{pathlib.Path().resolve()}/files/results-{filename}", "w") as result_file:
                result_file.write(
                    f"Case #{i}\n" + case(paths)
                )


def case(paths):
    direction = 1
    positions = [0, 1]
    max_width = [0, 0]
    max_height = [0, 0]
    enter_path, exit_path = paths.strip().upper().split()  # Убрали \n\r, перевели в верхний регистр, разделили

    # старт север
    for s in enter_path:
        direction = step(s, direction, positions, max_width, max_height)

    direction, max_width, max_height = end_path(direction, max_width, max_height)

    # [ North  South    West    East        ]
    # [ [true, false,   true,   false], ... ]
    rooms = [
        [
            [
                False for i in range(4)
            ] for row in range(max_height[1] - max_height[0] + 1)
        ] for col in range(max_width[1] - max_width[0] + 1)
    ]

    # возвращаемся
    for s in exit_path:
        direction = step(s, direction, positions, max_width, max_height)

        if s == "W":
            if direction == 0:
                try:
                    rooms[positions[0] - max_width[0]][positions[1] - max_height[0]][1] = True
                    rooms[positions[0] - max_width[0]][positions[1] - max_height[0] - 1][0] = True
                except Exception as error:
                    pass

            elif direction == 1:
                try:
                    rooms[positions[0] - max_width[0]][positions[1] - max_height[0]][0] = True
                    rooms[positions[0] - max_width[0]][positions[1] - max_height[0] + 1][0] = True
                except Exception as error:
                    pass

            elif direction == 2:
                try:
                    rooms[positions[0] - max_width[0]][positions[1] - max_height[0]][3] = True
                    rooms[positions[0] - max_width[0] + 1][positions[1] - max_height[0]][2] = True
                except Exception as error:
                    pass

            elif direction == 3:
                try:
                    rooms[positions[0] - max_width[0]][positions[1] - max_height[0]][2] = True
                    rooms[positions[0] - max_width[0] - 1][positions[1] - max_height[0]][3] = True
                except Exception as error:
                    pass

    direction, max_width, max_height = end_path(direction, max_width, max_height)

    # записываем результаты
    for i in range(max_height[1] - max_height[0], 0, -1):
        string = ""
        for j in range(max_width[1] - max_width[0] + 1):
            string += bool_to_hex(
                rooms[j][i][0],
                rooms[j][i][1],
                rooms[j][i][2],
                rooms[j][i][3],
            )
        print(string)
        string += "\n"
    return string


def step(symbol: str, direction: int, positions: list, max_width: list, max_height: list):
    if symbol == "W":
        position(direction, positions, max_width, max_height)
    elif symbol == "R":
        return rotation_r(direction)
    elif symbol == "L":
        return rotation_l(direction)
    return direction


def position(direction: int, positions: list, max_width: list, max_height: list):
    if direction == 0:
        positions[1] += 1
        if positions[1] > max_height[1]:
            max_height[1] += 1

    elif direction == 1:
        positions[1] -= 1
        if positions[1] < max_height[0]:
            max_height[0] -= 1

    elif direction == 2:
        positions[0] -= 1
        if positions[1] < max_width[0]:
            max_width[0] -= 1

    elif direction == 3:
        positions[0] += 1
        if positions[1] > max_width[1]:
            max_width[1] += 1


def rotation_r(direction: int):
    if direction == 0:
        direction = 3

    elif direction == 1:
        direction = 2

    elif direction == 2:
        direction = 0

    elif direction == 3:
        direction = 1

    return direction


def rotation_l(direction: int):
    if direction == 0:
        direction = 2

    elif direction == 1:
        direction = 3

    elif direction == 2:
        direction = 1

    elif direction == 3:
        direction = 0

    return direction


def end_path(direction, max_height, max_width):
    if direction == 0:
        direction = 1
        max_height[1] -= 1

    elif direction == 1:
        direction = 0
        max_height[0] += 1

    elif direction == 2:
        direction = 3
        max_width[0] += 1

    else:
        direction = 2
        max_width[1] -= 1

    return direction, max_width, max_height


def bool_to_hex(north: bool, south: bool, east: bool, west: bool):
    hex = 0

    if west:
        hex += 8
    if east:
        hex += 4
    if south:
        hex += 2
    if north:
        hex += 1

    if hex < 10:
        return str(hex)
    elif hex == 10:
        return "a"
    elif hex == 11:
        return "b"
    elif hex == 12:
        return "c"
    elif hex == 13:
        return "d"
    elif hex == 14:
        return "e"
    else:
        return "f"


if __name__ == "__main__":
    # тест должен лежать в папке tests
    filename = "large-test.in.txt"
    # выходной файл в results
    app(filename)

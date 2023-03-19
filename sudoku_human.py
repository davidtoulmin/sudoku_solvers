import re


# Read in sudoku
sudoku = [[{}]]*9
file = open("./input.txt", "r")
row_num = 0
for i in range(1, 12):
    if i % 4 == 0:
        file.readline()
        continue
    file_line = file.readline()
    # print(re.split('[ |]', file_line))
    sudoku[row_num] = [{'original': int(val), 'val': int(val), 'options': dict(map(lambda x: (x, True), range(1, 10)))}
                       for val in re.split('[ |]', file_line.strip())]
    row_num += 1


def update_surrounding_options(line_num, column_num):
    sudoku[line_num][column_num]['options'] = NO_OPTIONS
    square_val = sudoku[line_num][column_num]["val"]
    for i in range(9):
        if i != column_num:
            sudoku[line_num][i]["options"][square_val] = False
        if i != line_num:
            sudoku[i][column_num]["options"][square_val] = False
    for i in range(line_num // 3 * 3, line_num // 3 * 3 + 3):
        if i != line_num:
            for j in range(column_num // 3 * 3, column_num // 3 * 3 + 3):
                if j != column_num:
                    sudoku[i][j]["options"][square_val] = False


# Initialise sudoku notes
NO_OPTIONS = dict(map(lambda x: (x, False), range(1, 10)))
for line_num in range(9):
    for column_num in range(9):
        if sudoku[line_num][column_num]['val']:
            update_surrounding_options(line_num, column_num)


def print_sudoku():
    for line_count, line in enumerate(sudoku, start=1):
        for square_count, square in enumerate(line, start=1):
            print(square["val"], end='')
            if square_count%3 == 0 and square_count != 9:
                print('|', end='')
            else:
                print(' ', end='')
        print()
        if line_count%3 == 0 and line_count != 9:
            print("-----+-----+-----")
    print()

def print_options():
    for line_count, line in enumerate(sudoku, start=1):
        for i in range(0, 9, 3):
            for square_count, square in enumerate(line, start=1):
                for j in range(1, 4):
                    print(i+j if square["options"][i+j] else ' ', end='')
                print(' ', end='')
                if square_count % 3 == 0 and square_count != 9:
                    print('| ', end='')
            print()
        if line_count % 3 != 0:
            print("            |             |")
        elif line_count != 9:
            print("------------+-------------+------------")
    print()

print_sudoku()
print_options()
# print(sudoku)


def check_clash(line_num, column_num):
    for i in range(9):
        if i != column_num and sudoku[line_num][i]["val"] == sudoku[line_num][column_num]["val"]:
            return True
        if i != line_num and sudoku[i][column_num]["val"] == sudoku[line_num][column_num]["val"]:
            return True
    for i in range(line_num//3*3, line_num//3*3+3):
        if i != line_num:
            for j in range(column_num//3*3, column_num//3*3+3):
                if j != column_num:
                    if sudoku[i][j]["val"] == sudoku[line_num][column_num]["val"]:
                        return True
    return False


def choose_next_square(line_num, column_num):
    if column_num < 8:
        return line_num, column_num + 1
    return line_num + 1, 0


def is_solved():
    for i in range(9):
        for j in range(9):
            if sudoku[i][j]['val'] == 0:
                return False
    return True


def has_one_option(i, j):
    option = 0
    for num in range(1, 10):
        if sudoku[i][j]['options'][num]:
            if option:
                return False
            option = num
    return option


def is_only_square_in_row(i, j):
    for option, val in sudoku[i][j]['options'].items():
        if val:
            other_square = False
            for k in range(9):
                if k != i and sudoku[k][j]['options'][option]:
                    other_square = True
                    break
            if not other_square:
                return option
    return False


def is_only_square_in_column(i, j):
    for option, val in sudoku[i][j]['options'].items():
        if val:
            other_square = False
            for k in range(9):
                if k != j and sudoku[i][k]['options'][option]:
                    other_square = True
                    break
            if not other_square:
                return option
    return False


def is_only_square_in_box(i, j):
    for option, val in sudoku[i][j]['options'].items():
        if val:
            other_square = False
            for k in range(i // 3 * 3, i // 3 * 3 + 3):
                for l in range(j // 3 * 3, j // 3 * 3 + 3):
                    if not (k == i and l == j):
                        if sudoku[k][l]['options'][option]:
                            other_square = True
                            break
                if other_square:
                    break
            if not other_square:
                return option
    return False


def check_for_squares_in_line():
    for box_row in range(0, 9, 3):
        for box_column in range(0, 9, 3):
            box_options = dict(map(lambda x: (x, 0), range(1, 10)))
            for i in range(3):
                for j in range(3):
                    for num in range(1, 10):
                        if sudoku[box_row+i][box_column+j]['options'][num]:
                            box_options[num] += 1
                    # print(sudoku[box_row+i][box_column+j]['val'], end='')
            print(box_options)
            for num in range(1, 10):
                if 1 < box_options[num] < 4:



ittrs = 100
while not is_solved() and ittrs > 0:
    ittrs-=1
    for i in range(9):
        for j in range(9):
            for funct in (has_one_option, is_only_square_in_column, is_only_square_in_row, is_only_square_in_box):
                option = funct(i, j)
                if option:
                    sudoku[i][j]['val'] = option
                    update_surrounding_options(i, j)
                    break


# check_next_square(0, 0)
print_sudoku()
check_for_squares_in_line()


def print_errors():
    for i in range(9):
        for j in range(9):
            if check_clash(i, j):
                print(i, j, sudoku[i][j]['val'])
            if sudoku[i][j]["original"] and sudoku[i][j]["original"] != sudoku[i][j]["val"]:
                print(i, j)

# print_errors()

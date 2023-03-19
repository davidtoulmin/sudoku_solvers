import re

sudoku = [[]]*9

file = open("./input.txt", "r")
row_num = 0
for i in range(1,12):
	if i%4==0:
		file.readline()
		continue
	file_line = file.readline()
	sudoku[row_num] = [int(val) for val in re.split('[ |]', file_line.strip())]
	row_num+=1

def print_sudoku():
	for line_count, line in enumerate(sudoku, start=1):
		for square_count, square in enumerate(line, start=1):
			print(square, end='')
			if square_count%3 == 0 and square_count != 9:
				print('|', end='')
			else:
				print(' ', end='')
		print()
		if line_count%3 == 0 and line_count != 9:
			print("-----+-----+-----")
	print()

print_sudoku()

def check_clash(line_num, column_num):
	for i in range(9):
		if i != column_num and sudoku[line_num][i] == sudoku[line_num][column_num]:
			return True
		if i != line_num and sudoku[i][column_num] == sudoku[line_num][column_num]:
			return True
	for i in range(line_num//3*3, line_num//3*3+3):
		if i != line_num:
			for j in range(column_num//3*3, column_num//3*3+3):
				if j != column_num:
					if sudoku[i][j] == sudoku[line_num][column_num]:
						return True
	return False


def choose_next_square(line_num, column_num):
	if column_num < 8:
		return line_num, column_num + 1
	return line_num + 1, 0

def check_next_square(line_num, column_num):
	if(line_num >= 9):
		return True
	if sudoku[line_num][column_num]:
		return check_next_square(*choose_next_square(line_num, column_num))
	for val in range(1,10):
		sudoku[line_num][column_num] = val
		if not check_clash(line_num, column_num):
			if check_next_square(*choose_next_square(line_num, column_num)):
				return True
	sudoku[line_num][column_num] = 0
	return False

check_next_square(0,0)
print_sudoku()

for i in range(9):
	for j in range(9):
		if check_clash(i, j):
			print(i, j)

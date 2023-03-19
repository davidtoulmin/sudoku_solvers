import re

sudoku = [[]]*9

file = open("./input.txt", "r")
row_num = 0
for i in range(1,12):
	if i%4==0:
		file.readline()
		continue
	file_line = file.readline()
	sudoku[row_num] = [{'original': int(val), 'val': int(val), 'touches': 0, 'assigns': 0, 'backtracks': 0} for val in re.split('[ |]', file_line.strip())]
	row_num+=1

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

print_sudoku()

def check_clash(line_num, column_num):
	for i in range(9):
		sudoku[line_num][i]["touches"] += 1
		sudoku[line_num][column_num]["touches"] += 1
		if i != column_num and sudoku[line_num][i]["val"] == sudoku[line_num][column_num]["val"]:
			return True
		sudoku[i][column_num]["touches"] += 1
		sudoku[line_num][column_num]["touches"] += 1
		if i != line_num and sudoku[i][column_num]["val"] == sudoku[line_num][column_num]["val"]:
			return True
	for i in range(line_num//3*3, line_num//3*3+3):
		if i != line_num:
			for j in range(column_num//3*3, column_num//3*3+3):
				if j != column_num:
					sudoku[i][j]["touches"] += 1
					sudoku[line_num][column_num]["touches"] += 1
					if sudoku[i][j]["val"] == sudoku[line_num][column_num]["val"]:
						return True
	return False

def choose_next_square(line_num, column_num):
	if column_num < 8:
		return line_num, column_num + 1
	return line_num + 1, 0

def solve_sudoku():
	count = 0
	checked_squares = []
	line_num = column_num = 0
	while(line_num < 9):
		count += 1
		sudoku[line_num][column_num]["touches"] += 1
		if not sudoku[line_num][column_num]["original"]:
			if sudoku[line_num][column_num]["val"] < 9:
				sudoku[line_num][column_num]["val"] += 1
				sudoku[line_num][column_num]["assigns"] += 1
				if not check_clash(line_num, column_num):
					checked_squares.append([line_num, column_num])
					line_num, column_num = choose_next_square(line_num, column_num)
			else:
				sudoku[line_num][column_num]["assigns"] += 1
				sudoku[line_num][column_num]["backtracks"] += 1
				sudoku[line_num][column_num]["val"] = 0
				line_num, column_num = checked_squares.pop()
		else:
			line_num, column_num = choose_next_square(line_num, column_num)
	print(count)


solve_sudoku()
print_sudoku()


def print_sudoku_touches():
	count = 0
	for line_count, line in enumerate(sudoku, start=1):
		for square_count, square in enumerate(line, start=1):
			print('%6s' % str(square["touches"]), end=', ')
			count += square["touches"]
			# if square_count%3 == 0 and square_count != 9:
			# 	print('|', end='')
			# else:
			# 	print(' ', end='')
		print()
		# if line_count%3 == 0 and line_count != 9:
			# print("--------------------+--------------------+--------------------")
	print(count)
	print()

print_sudoku_touches()

def print_sudoku_assigns():
	count = 0
	for line_count, line in enumerate(sudoku, start=1):
		for square_count, square in enumerate(line, start=1):
			print('%5s' % str(square["assigns"]), end=', ')
			count += square["assigns"]
			# if square_count%3 == 0 and square_count != 9:
			# 	print('|', end='')
			# else:
			# 	print(' ', end='')
		print()
		# if line_count%3 == 0 and line_count != 9:
			# print("-----------------+-----------------+-----------------")
	print(count)
	print()

print_sudoku_assigns()

def print_sudoku_backtracks():
	count = 0
	for line_count, line in enumerate(sudoku, start=1):
		for square_count, square in enumerate(line, start=1):
			print('%5s' % str(square["backtracks"]), end=', ')
			count += square["backtracks"]
			# if square_count%3 == 0 and square_count != 9:
			# 	print('|', end='')
			# else:
			# 	print(' ', end='')
		print()
		# if line_count%3 == 0 and line_count != 9:
			# print("-----------------+-----------------+-----------------")
	print(count)
	print()

print_sudoku_backtracks()

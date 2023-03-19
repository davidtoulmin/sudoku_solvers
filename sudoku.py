import re

sudoku = [[]]*9

file = open("./input.txt", "r")
row_num = 0
for i in range(1,12):
	if i%4==0:
		file.readline()
		continue
	file_line = file.readline()
	# print(re.split('[ |]', file_line))
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
# print(sudoku)

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


# for line_num, line in enumerate(sudoku):
# 	for column_num, square in enumerate(line):
# 		if not square["original"]:
# 			for i in range(1,10):
# 				square["val"]=i

def choose_next_square(line_num, column_num):
	if column_num < 8:
		return line_num, column_num + 1
	return line_num + 1, 0

def check_next_square(line_num, column_num):
	if(line_num >= 9):
		return True
	sudoku[line_num][column_num]["touches"] += 1
	if not sudoku[line_num][column_num]["original"]:
		for val in range(1,10):
			sudoku[line_num][column_num]["assigns"] += 1
			sudoku[line_num][column_num]["val"] = val
			if not check_clash(line_num, column_num):
				if check_next_square(*choose_next_square(line_num, column_num)):
					return True
		sudoku[line_num][column_num]["assigns"] += 1
		sudoku[line_num][column_num]["backtracks"] += 1
		sudoku[line_num][column_num]["val"] = 0
	else:
		if check_next_square(*choose_next_square(line_num, column_num)):
			return True
	return False

check_next_square(0,0)
print_sudoku()

# print(check_clash(4,5))

# def foo(a, b):
# 	if(a >= 9):
# 		print("here")
# 		return
# 	print(a, b, sudoku[a][b]["val"])
# 	foo(*choose_next_square(a, b))

# foo(0,0)
for i in range(9):
	for j in range(9):
		if check_clash(i, j):
			print(i, j)
		if sudoku[i][j]["original"] and sudoku[i][j]["original"] != sudoku[i][j]["val"]:
			print(i, j)
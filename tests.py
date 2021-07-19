def isValid(board):
	for num in range(1,10):
		# lines
		for line in board:
			if line.count(num) > 1:
				return False
		# columns
		boardT = [[row[i] for row in board] for i in range(9)]
		for line in boardT:
			if line.count(num) > 1:
				return False
		# small squares
		squares = subSquares(board)
		for square in squares:
			squishedSquare = [item for line in square for item in line]

			if squishedSquare.count(num) > 1:
				return False

	return True

def subSquares(sudoku):
	squares = []

	for i in range(3):
		for j in range(3):
			square = [[sudoku[r][c] for c in range(j*3, (j*3)+3)] for r in range(i*3, (i*3)+3)]
			squares.append(square)
	return squares

def createSkeleton(sudoku):
	'''returns a skeleton of the sudoku to fill later'''
	skeleton = []
	for i, line in enumerate(sudoku):
		skeleton.append([])
		for j, row in enumerate(line):
			if row != ' ':
				skeleton[i].append(row)
			else:
				skeleton[i].append(list())

	return skeleton

def getPossibles(sudoku):
	'''returns a sudoku with lists with the possible numbers 
	that can go in that position'''
	possibles = createSkeleton(sudoku)

	for i, line in enumerate(sudoku):
		for j, row in enumerate(line):
			if row != ' ':
				pass
			else:
				for num in range(1, 10):
					newSudoku = [list(line) for line in sudoku]
					newSudoku[i][j] = num
					if isValid(newSudoku):
						possibles[i][j].append(num)
	return possibles

def isFull(sudoku):
	if not isValid(sudoku):
		return False

	for i in sudoku:
		if ' ' in i:
			return False
	return True

def solveSudoku(sudoku):
	if isFull(sudoku):
		return sudoku
	possibles = getPossibles(sudoku)

	# checks for squares with only one possible number
	for i, line in enumerate(possibles):
		for j, item in enumerate(line): 
			if type(item) == list and len(item) == 1:
				newSudoku = [list(line) for line in sudoku]
				newSudoku[i][j] = item[0]
				# solveSudoku(newSudoku)
				return newSudoku

	# if there's no square with only one possible number, do this

	for num in range(1,10):
		# lines
		appeared = []
		
		for i, line in enumerate(possibles):
			for j, item in enumerate(line):
				if type(item) == list and num in item:
					appeared.append((i, j))

		if len(appeared) == 1:
			i, j = appeared[0]
			newSudoku = [list(line) for line in sudoku]
			newSudoku[i][j] = num
			return newSudoku
		
		# columns
		appeared = []
		sudokuT = [[row[i] for row in possibles] for i in range(9)]
		
		for i, line in enumerate(sudokuT):
			for j, item in enumerate(line):
				if type(item) == list and num in item:
					appeared.append((j, i))

		if len(appeared) == 1:
			i, j = appeared[0]
			newSudoku = [list(line) for line in sudoku]
			newSudoku[i][j] = num
			return newSudoku
		
		# small squares
		# i hate this thing
		squares = subSquares(possibles)
		
		for k, square in enumerate(squares):
			appeared = []

			for i, line in enumerate(square):
				for j, item in enumerate(line):
					if type(item) == list and num in item:
						appeared.append((k//3*3 + i, k%3*3 + j))
			
			if len(appeared) == 1:
				i, j = appeared[0]
				newSudoku = [list(line) for line in sudoku]
				newSudoku[i][j] = num
				return newSudoku
		

	
board = [
		[ 4 ,' ', 9 , 1 , 7 , 8 , 6 ,' ',' '],
		[' ', 5 , 1 , 3 , 9 , 6 ,' ',' ',' '],
		[' ', 6 , 7 , 4 , 2 , 5 ,' ', 1 ,' '],
		[ 6 ,' ', 8 ,' ',' ',' ',' ',' ',' '],
		[ 9 ,' ', 2 ,' ',' ',' ', 3 , 6 ,' '],
		[' ',' ', 5 , 6 ,' ',' ',' ',' ', 1 ],
		[' ',' ', 4 , 5 ,' ',' ',' ',' ', 6 ],
		[' ',' ', 6 , 2 ,' ',' ', 1 ,' ', 4 ],
		[' ',' ', 3 ,' ', 6 , 4 ,' ',' ', 7 ]]



board = solveSudoku(board)





for i in board:
	print (i)

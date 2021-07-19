import pygame

'''
TO DO: 
solver algorithm
generator algorithm
'''

board = [[' ' for i in range(9)] for i in range(9)]
board = [
	[ 6 , 2 ,' ', 9 ,' ',' ',' ',' ',' '],
	[' ',' ', 9 ,' ',' ',' ',' ', 5 , 2 ],
	[' ',' ',' ', 7 ,' ', 1 , 9 ,' ',' '],
	[' ',' ',' ', 6 ,' ',' ',' ', 1 ,' '],
	[ 4 ,' ', 6 ,' ', 1 ,' ',' ', 7 ,' '],
	[' ',' ',' ',' ', 3 , 2 ,' ',' ',' '],
	[ 1 , 7 ,' ',' ',' ', 8 ,' ',' ',' '],
	[ 3 ,' ',' ',' ',' ',' ', 5 ,' ',' '],
	[' ', 8 ,' ',' ',' ', 6 ,' ',' ', 1 ]]


numberInputs = {
	pygame.K_1:1,
	pygame.K_2:2,
	pygame.K_3:3,
	pygame.K_4:4,
	pygame.K_5:5,
	pygame.K_6:6,
	pygame.K_7:7,
	pygame.K_8:8,
	pygame.K_9:9
	}

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
		# i hate this thing
		for i in range(3):
			for j in range(3):
				square = [board[r][c] for c in range(j*3, (j*3)+3) for r in range(i*3, (i*3)+3)]
				if square.count(num) > 1:
					return False
	return True

class Game:
	def __init__(self, res:tuple, fps:int) -> None:
		pygame.init()

		self.w, self.h = res
		self.fps = fps

		self.screen = pygame.display.set_mode(res)
		self.font = pygame.font.Font(None, 36)
		self.clock = pygame.time.Clock()
		self.selected = None
		self.run = True
		self.margins = 50
		self.squareSize = (self.w - (2*self.margins))/9

	# secondary functions 
	def drawLines(self):
		margins = self.margins
		# vertical
		for i in range(10):
			start = (self.squareSize*i+margins, margins)
			end = (self.squareSize*i+margins, self.h-margins)
			pygame.draw.aaline(self.screen, (0,0,0), start, end)
		# horizontal
		for i in range(10):
			start = (margins, self.squareSize*i+margins)
			end = (self.w-margins, self.squareSize*i+margins) 
			pygame.draw.aaline(self.screen, (0,0,0), start, end)

	def drawNumbers(self, sudoku):
		start = self.margins*1.6

		for i, line in enumerate(sudoku):
			for j, num in enumerate(line):
				number = self.font.render(str(num), True, (0,0,0))
				rect = number.get_rect()
				rect.center = (start+(j*self.squareSize), start+(i*self.squareSize))

				self.screen.blit(number, rect)

	def selectSquare(self, mousePos):
		x, y = mousePos
		
		if self.margins<x<self.squareSize*9+self.margins and self.margins<y<self.squareSize*9+self.margins:
			xSquare = (x-self.margins)//self.squareSize
			ySquare = (y-self.margins)//self.squareSize

			self.selected = (int(xSquare), int(ySquare))
		else:
			self.selected = None
		
	def highlight(self):
		if self.selected:
			pos = (self.selected[0] * self.squareSize + self.margins, self.selected[1] * self.squareSize + self.margins)

			highlight = pygame.Rect(pos , (self.squareSize, self.squareSize))
			pygame.draw.rect(self.screen, (0,200,0), highlight)

	def placeNumber(self, number, sudoku):
		if not self.selected:
			return 
		
		column, row = self.selected
		newSudoku = [list(line) for line in sudoku]
		newSudoku[row][column] = number
		if isValid(newSudoku):
			sudoku[row][column] = number
			
		self.selected = None

	# main functions 
	def events(self):
		mousePos = pygame.mouse.get_pos()
		for event in pygame.event.get():
			if event.type == pygame.QUIT: # closes the game
				self.run = False
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE: # closes the game too
					self.run = False
				elif event.key in numberInputs: # number input 
					self.placeNumber(numberInputs[event.key], board)
			elif event.type == pygame.MOUSEBUTTONDOWN:
				self.selectSquare(mousePos)

	def updates(self):
		self.screen.fill((255,255,255))
		self.highlight()
		self.drawLines()
		self.drawNumbers(board)

		pygame.display.update()

	def main(self):
		while self.run:
			self.events()
			self.updates()
			self.clock.tick(self.fps)
	
if __name__ == '__main__':
	game = Game((650, 650), 60)
	game.main()
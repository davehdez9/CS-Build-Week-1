import math
from random import random
from adventure.models import Room

# Pretty much copied line for line from 
# https://codepen.io/anon/pen/aLpORx

class Grid:
	def __init__(self, dimensions=20, maxTunnels=100, maxLength=5):
		self.dimensions = dimensions
		self.maxTunnels = maxTunnels
		self.maxLength = maxLength
		self.grid = self.createGrid(dimensions) # Create the grid

		self.currentRow = math.floor(random() * dimensions) # random start X
		self.currentCol = math.floor(random() * dimensions) # random start Y
		self.directions = [[0, -1], [1, 0], [0, 1], [-1, 0]] # top, right, bottom, left
		self.lastDirection = [0, 0] # save the last direction
		self.randomDirection = [0, 0]

	def createGrid(self, dimensions, num=0 ):
		# Create an empty array and init with all "walls"
		a = []
		for i in range(0, dimensions):
			a.append([])
			for j in range(0, dimensions):
				a[i].append(num)
		return a

	def carveGrid(self):
		# while we haven't hit the max Tunnels allowed
		while self.maxTunnels > 0:

			# Check that the nextDirection is perpendicular to the lastDirection
			# TODO: the above... next line is temporary
			while (self.randomDirection[0] == -self.lastDirection[0] and self.randomDirection[1] == -self.lastDirection[1]) or (self.randomDirection[0] == self.lastDirection[0] and self.randomDirection[1] == self.lastDirection[1]):
				# Get a random direction
				self.randomDirection = self.directions[math.floor(random() * 4)]

			# Move a random distance in a particular direction
			randomLength = math.ceil(random() * self.maxLength)
			tunnelLength = 0

			while tunnelLength < randomLength:
				# Moving up, moving 
				if not ((self.currentRow == 0 and self.randomDirection[0] == -1) or (self.currentCol == 0 and self.randomDirection[1] == -1) or (self.currentRow == self.dimensions - 1 and self.randomDirection[0] == 1 ) or (self.currentCol == self.dimensions - 1 and self.randomDirection[1] == 1)):

					self.grid[self.currentRow][self.currentCol] = 1
					self.currentRow += self.randomDirection[0]
					self.currentCol += self.randomDirection[1]
					tunnelLength += 1	
				
				else:
					break

			if tunnelLength >= 0:
				self.lastDirection = self.randomDirection
				self.maxTunnels -= 1


myGrid = Grid()
myGrid.carveGrid()
print(' ')
for i in myGrid.grid:
	print(i)

total = 0
for i in range(0, len(myGrid.grid)):
	for j in myGrid.grid[i]:
		

print('Total', total)	

# grid = [None, None, None, None, None, None, None, None, None]
# grid = [ 0,     1,    2,    3,    4,   5,     6,    7,    8 ]
# grid = [None, Room, None, Room, Room, Room, None, None, Room]

# grid = [
#   None, Room, None, 
#   Room, Room, Room,
#   None, None, Room,
# ]


# grid = [
#   [None, Room, None],
#   [Room, Room, Room],
#   [None, None, Room]
# ]


# grid[1][0] = Room
# x = row
# y = column

# grid[1][1]

# def get_neighbors(x, y):
#   # First condition is at edge of map
#   # second is if it's a wall
#   neighbors = [None, None, None, None] # Top, Right, Bottom, Left

#   if not x - 1 < 0 or grid[x - 1][y] is not None:
#     neighbors[0] = grid[x - 1][y]
  
#   if not y + 1 > row or grid[x][y + 1] is not None:
#     neighbors[1] = grid[x][y + 1]
  
#   if not x + 1 > col or grid[x + 1][y] is not None:
#     neighbors[2] = grid[x + 1][y]
  
#   if not y - 1 < 0 or grid[x][y - 1] is not None:
#     neighbors[3] = grid[x][y - 1]

#   return neighbors

# def get_direction(i):
#   switch (i):
#     case 0:
#       return 'n'
#     case 1:
#       return 'r'
#     case 2:
#       return ''

# for x in cols:
#   for y in rows:

#     # Check if it's a room
#     if grid[x][y] is not None:
#       neighbors = get_neighbors(x, y)

#       for i in neighbors:
#         if i is not None:
#           grid[x][y].connectRooms(neighbors[i], get_direction(i))
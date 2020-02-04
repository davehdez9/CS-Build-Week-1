

grid = [None, None, None, None, None, None, None, None, None]
grid = [ 0,     1,    2,    3,    4,   5,     6,    7,    8 ]
grid = [None, Room, None, Room, Room, Room, None, None, Room]

grid = [
  None, Room, None, 
  Room, Room, Room,
  None, None, Room,
]


grid = [
  [None, Room, None],
  [Room, Room, Room],
  [None, None, Room]
]


grid[1][0] = Room
x = row
y = column

grid[1][1]

def get_neighbors(x, y):
  # First condition is at edge of map
  # second is if it's a wall
  neighbors = [None, None, None, None] # Top, Right, Bottom, Left

  if not x - 1 < 0 or grid[x - 1][y] is not None:
    neighbors[0] = grid[x - 1][y]
  
  if not y + 1 > row or grid[x][y + 1] is not None:
    neighbors[1] = grid[x][y + 1]
  
  if not x + 1 > col or grid[x + 1][y] is not None:
    neighbors[2] = grid[x + 1][y]
  
  if not y - 1 < 0 or grid[x][y - 1] is not None:
    neighbors[3] = grid[x][y - 1]

  return neighbors

def get_direction(i):
  switch (i):
    case 0:
      return 'n'
    case 1:
      return 'r'
    case 2:
      return ''

for x in cols:
  for y in rows:

    # Check if it's a room
    if grid[x][y] is not None:
      neighbors = get_neighbors(x, y)

      for i in neighbors:
        if i is not None:
          grid[x][y].connectRooms(neighbors[i], get_direction(i))
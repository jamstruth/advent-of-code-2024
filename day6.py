from pprint import pprint
from enum import Enum

class GuardStatus(Enum):
  ON_MAP = 1
  OFF_MAP = 2

class Direction(Enum):
  NORTH = 1
  EAST = 2
  SOUTH = 3
  WEST = 4

class Obstacle:
  def __init__(self, location: tuple):
    self.location = location

class Map:
  def __init__(self, dimensions: tuple, obstacles: list):
    self.dimensions = dimensions
    self.obstacles = obstacles

  def is_coord_obstacle(self, location):
    for obstacle in self.obstacles:
      if obstacle.location == location:
        return True
    return False
  
  def is_coord_on_map(self, location):
    (target_x, target_y) = location
    (x_dim, y_dim) = self.dimensions
    return (target_x >= 0 and target_x < x_dim) and (target_y >= 0 and target_y < y_dim)

class Guard:
  def __init__(self, direction: Direction, location: tuple, map: Map):
    self.direction = direction
    self.location = location
    self.status = GuardStatus.ON_MAP
    self.map = map

  def move(self):
    target_location = self.determine_target_move()
    print(f"Trying to move to {target_location}")
    if (self.map.is_coord_on_map(target_location)):
      if (self.map.is_coord_obstacle(target_location)):
        # If there's an obstacle we need to turn and try again
        print(f"{target_location} is obstacle, turning and retrying")
        self.turn_right()
        return self.move()
      else:
        print(f"Moving to {target_location}")
        self.location = target_location
    else:
      print('Moving Off Map')
      self.status = GuardStatus.OFF_MAP
      self.location = None

  def determine_target_move(self):
    match self.direction:
      case Direction.NORTH:
        return (self.location[0], self.location[1]-1)
      case Direction.SOUTH:
        return (self.location[0], self.location[1]+1)
      case Direction.WEST:
        return (self.location[0]-1, self.location[1])
      case Direction.EAST:
        return (self.location[0]+1, self.location[1])
      
  def turn_right(self):
    match self.direction:
      case Direction.NORTH:
        self.direction = Direction.EAST
      case Direction.SOUTH:
        self.direction = Direction.WEST
      case Direction.WEST:
        self.direction = Direction.NORTH
      case Direction.EAST:
        self.direction = Direction.SOUTH

  
def determine_guard_dir(char):
  if(char == '^'):
    return Direction.NORTH
  if(char == '>'):
    return Direction.EAST
  if(char == 'v'):
    return Direction.SOUTH
  if(char == '<'):
    return Direction.WEST

def parse_input_to_guard(input_file):
  guard_symbols = ['^', '>', 'v', '<']
  with open(input_file, "r") as input:
    lines = input.read().splitlines()
    x_dim = len(lines[0])
    y_dim = len(lines)
    guard_x = None
    guard_y = None
    guard_dir = None
    obstacles = []
    for y_coord, line in enumerate(lines):
      for x_coord, char in enumerate(line):
        if char == '#':
          # Build Obstacle
          print((x_coord, y_coord))
          obstacles.append(Obstacle(location=(x_coord, y_coord)))
          continue
        if char in guard_symbols:
          guard_x = x_coord
          guard_y = y_coord
          guard_dir = determine_guard_dir(char)
    map = Map(dimensions=(x_dim, y_dim), obstacles=obstacles)
    return Guard(direction=guard_dir, location=(guard_x, guard_y), map=map)


INPUT_FILE = 'inputs/day6_input'
guard = parse_input_to_guard(INPUT_FILE)
guard_locations = {guard.location}

print(f"There is an obstacle at (4,0): {guard.map.is_coord_obstacle((4, 0))}")
print(f"(-1, 0) is on map: {guard.map.is_coord_on_map((-1, 0))}")
print(f"(0, -1) is on map: {guard.map.is_coord_on_map((0, -1))}")
(x_dim, y_dim) = guard.map.dimensions
print(f"({x_dim}, 0) is on map: {guard.map.is_coord_on_map((x_dim, 0))}")
print(f"(0, {y_dim}) is on map: {guard.map.is_coord_on_map((0, y_dim))}")
print(f"(1, 5) is on map: {guard.map.is_coord_on_map((1, 5))}")

# Move guard until his status is OFF_MAP
# Note his movements
while(guard.status == GuardStatus.ON_MAP):
  print(f"Guard at: {guard.location}")
  guard.move()
  if(guard.location != None):
    guard_locations.add(guard.location)

print(f"Guard Visited {len(guard_locations)} unique locations")
from pprint import pprint
from enum import Enum

class GuardStatus(Enum):
  NORMAL = 1
  OFF_MAP = 2
  LOOPED = 3

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
    self.start_location = location
    self.start_direction = direction
    self.direction = direction
    self.location = location
    self.status = GuardStatus.NORMAL
    self.map = map

  def check_has_looped(self):
     return self.location == self.start_location and self.direction == self.start_direction

  def move(self):
    if(self.status == GuardStatus.NORMAL):
      target_location = self.determine_target_move()
      if (self.map.is_coord_on_map(target_location)):
        self.perform_move(target_location)
        if self.check_has_looped():
          print('Guard looped!')
          self.status = GuardStatus.LOOPED
      else:
        print('Moving Off Map')
        self.status = GuardStatus.OFF_MAP
        self.location = None

  def perform_move(self, target_location):
    if (self.map.is_coord_obstacle(target_location)):
      # If there's an obstacle we need to turn and try again
      self.turn_right()
      return self.move()
    else:
      self.location = target_location

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
          obstacles.append(Obstacle(location=(x_coord, y_coord)))
          continue
        if char in guard_symbols:
          guard_x = x_coord
          guard_y = y_coord
          guard_dir = determine_guard_dir(char)
    map = Map(dimensions=(x_dim, y_dim), obstacles=obstacles)
    return Guard(direction=guard_dir, location=(guard_x, guard_y), map=map)


INPUT_FILE = 'inputs/day6_practice'
guard = parse_input_to_guard(INPUT_FILE)
guard_locations = {guard.location}

# Move guard until his status is OFF_MAP
# Note his movements
while(guard.status != GuardStatus.OFF_MAP):
  print(f"Guard at: {guard.location}")
  guard.move()
  if(guard.location != None):
    guard_locations.add(guard.location)
print(f"Guard Visited {len(guard_locations)} unique locations")

# Simulate lots of guards adding a new object in each location and count how many cause a loop
initial_guard = parse_input_to_guard(INPUT_FILE)
loop_count = 0
(x_dim, y_dim) = initial_guard.map.dimensions
for x in range(x_dim):
  for y in range(y_dim):
    print(f"Trying obstacle at {(x, y)}")
    if(initial_guard.location == (x, y) or initial_guard.map.is_coord_obstacle((x, y))):
      continue # Skip any existing obstacles and the guard
    new_obstacles = [Obstacle(location=(x, y))]
    curr_map = Map(dimensions=initial_guard.map.dimensions, obstacles=initial_guard.map.obstacles[:]+new_obstacles)
    curr_guard = Guard(direction=initial_guard.direction, location=initial_guard.location, map=curr_map)
    while(curr_guard.status == GuardStatus.NORMAL):
      # print(f"Current Guard at: {curr_guard.location}")
      # print(f"Current Guard status: {curr_guard.status}")
      curr_guard.move()
    if (curr_guard.status == GuardStatus.LOOPED):
      loop_count += 1
print(f"There are {loop_count} obstacle locations that cause a loop")
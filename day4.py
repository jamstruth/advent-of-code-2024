from pprint import pprint

INPUT_FILE = "inputs/day4_input"
XMAS = 'XMAS'
SAMX = 'SAMX'

# Then lets load this into a 2D array
character_matrix = []
with open(INPUT_FILE, "r") as input:
  for line in input.read().splitlines():
    character_matrix.append(list(line)) # -1 Drops \n character

# Now we start searching
total_xmas = 0

step_value = len(XMAS)-1 # Step value stops us going off the side for down + down-right directions
for row in range(len(character_matrix)-step_value):
  for col in range(len(character_matrix[0])-step_value):
    # Build Strings
    right_string = ""
    down_string = ""
    down_right_string = ""
    down_left_string = ""
    for offset in range(len(XMAS)):
      right_string += character_matrix[row][col+offset]
      down_string += character_matrix[row+offset][col]
      down_right_string += character_matrix[row+offset][col+offset]
      if(col-offset > 0):
        down_left_string += character_matrix[row+offset][col-offset]
    all_strings = [right_string,down_string,down_right_string,down_left_string]
    for string in all_strings:
      if string == XMAS or string == SAMX:
        total_xmas += 1

print(f"All Xmas is {total_xmas}")
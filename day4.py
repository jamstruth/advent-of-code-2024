from pprint import pprint
import re

INPUT_FILE = "inputs/day4_input"
XMAS = 'XMAS'
SAMX = 'SAMX'

def search_for_xmas(lines):
  total_xmas = 0
  for line in lines:
    total_xmas += len(re.findall(XMAS, line))
    total_xmas += len(re.findall(SAMX, line))
  return total_xmas

# First find Horizontal ones because that's easiest...
with open(INPUT_FILE, "r") as input:
  horizontal_xmas = search_for_xmas(input.readlines())

print(f"Found {horizontal_xmas} occurrences horizontally")

# Then lets load this into a 2D array
character_matrix = []
with open(INPUT_FILE, "r") as input:
  for line in input.readlines():
    character_matrix.append(list(line)[:-1]) # -1 Drops \n character

# Work with the columns
column_strings = [""]*len(character_matrix)
for row in character_matrix:
  for index, col_char in enumerate(row):
    column_strings[index] += col_char
column_xmas = search_for_xmas(column_strings)
print(f"Found {column_xmas} occurrences vertically")

# Work with the diagonals range(len(character_matrix)
right_diagonal_strings = []
for start_row_index in range(3):
  for start_col_index in range(len(character_matrix[0])):
    if (start_row_index != 0 and start_col_index >= start_row_index):
      break
    diagonal_string = ""
    for row_index in range(start_row_index, len(character_matrix)):
      target_column = (row_index - start_row_index) + start_col_index
      if (target_column < len(character_matrix[0])):
        print(f"Adding [{row_index}][{target_column}]")
        diagonal_string += character_matrix[row_index][target_column]
    right_diagonal_strings.append(diagonal_string)
pprint(f"Expected {1+(138*2)} right_diagonal_strings, got {len(right_diagonal_strings)}")
right_diagonal_xmas = search_for_xmas(right_diagonal_strings)


def parse_input_file():
  lines = []
  with open("inputs/day1_input", "r") as input:
    lines = input.readlines()
  left_list = []
  right_list = []
  for line in lines:
    [left_num, right_num] = line.split('   ')
    left_list.append(int(left_num))
    right_list.append(int(right_num))
  return left_list, right_list

left_list, right_list = parse_input_file()
print(f"Left List Length: {len(left_list)} Right List Length: {len(right_list)}")
left_list.sort()
right_list.sort()

total_difference = 0
for left, right in zip(left_list, right_list):
  total_difference += (abs(left - right))
print(f"Total Difference between Left+Right: {total_difference}")

similarity_score = 0
for left in left_list:
  for right in right_list:
    if left == right:
      similarity_score += left

print(f"Similarity Score: {similarity_score}")
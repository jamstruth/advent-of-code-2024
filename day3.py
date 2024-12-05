import re
from pprint import pprint

mul_regex = 'mul\\(\\d+,\\d+\\)'
mul_numbers_regex = '\\d+,\\d+'
do_regex = 'do\\(\\)'
dont_regex = 'don\\\'t\\(\\)'

def read_input_string():
  with open("inputs/day3_input", "r") as input:
      return input.read()
  
def parse_and_perform_multiply(mul_func):
  [left_str, right_str]= re.findall(mul_numbers_regex, mul_func)[0].split(',')
  return int(left_str) * int(right_str)

input_memory = read_input_string()

print("Without Conditional Statements")
mul_func_strings = re.findall(mul_regex, input_memory)
result = 0
for mul_func in mul_func_strings:
    result += parse_and_perform_multiply(mul_func)
print(f"Total Result is: {result}")

print("With Conditional Statements")
all_func_strings = re.findall(f"{mul_regex}|{do_regex}|{dont_regex}", input_memory)
multiply_enabled = True # Assume works to start (can change if wrong)
conditional_result = 0
for function in all_func_strings:
  if re.search(do_regex, function) is not None:
     multiply_enabled = True
  if re.search(dont_regex, function) is not None:
     multiply_enabled = False
  if multiply_enabled and re.search(mul_regex, function) is not None:
     conditional_result += parse_and_perform_multiply(function)
print(f"Total Result is: {conditional_result}")
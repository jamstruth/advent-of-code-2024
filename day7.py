
from enum import Enum
from itertools import combinations_with_replacement

class Operator(Enum):
  ADD = 0
  MULTIPLY = 1

class Equation:
  def __init__(self, answer: int, numbers: list):
    self.answer = answer
    self.numbers = numbers

  def is_possible_equation(self):
    # Determine number of positions
    number_of_operators = len(self.numbers) - 1
    operators = [o.value for o in Operator]
    for i in range((1 << number_of_operators)):
      bits = [(i >> bit) & 1 for bit in range(number_of_operators - 1, -1, -1)]
      # calculate with these operators
      result = self.perform_calculation(operators=bits)
      if result == self.answer:
        print(f"{bits} matched answer for numbers {self.numbers}")
        return True
    print(f"No match found for numbers {self.numbers} for answer {self.answer}")
    return False
      
  def perform_calculation(self, operators):
    answer = self.numbers[0]
    for index, operator in enumerate(operators):
      if (operator == Operator.ADD.value):
        answer += self.numbers[index+1]
      if (operator == Operator.MULTIPLY.value):
        answer *= self.numbers[index+1]
    return answer


def parse_file(input_file):
  equations = []
  with open(input_file, "r") as file:
    for line in file.readlines():
      [answer_str, numbers_str] = line.split(': ')
      number_strs = numbers_str.split(' ')
      numbers = list(map(int, number_strs))
      equations.append(Equation(answer=int(answer_str), numbers=numbers))
  return equations

INPUT_FILE = 'inputs/day7_practice'
equations = parse_file(INPUT_FILE)
total_calibration = 0
for equation in equations:
  if equation.is_possible_equation():
    total_calibration += equation.answer

print(f"Total Calibration Result: {total_calibration}")
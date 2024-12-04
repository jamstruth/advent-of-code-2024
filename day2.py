import pprint

def parse_input_file():
  with open("inputs/day2_input", "r") as input:
    lines = input.readlines()
    reports = []
    for line in lines:
      reports.append(list(map(lambda numstring: int(numstring), line.split(' '))))
    return reports
  

def determine_report_safety(report):
  ascending = None
  previous_report_num = None
  for index, report_num in enumerate(report):
    # If Previous in None we haven't done anything yet
    if previous_report_num is not None:
      difference = previous_report_num - report_num
      # This is the easiest check so do it first.
      if(abs(difference) > 3):
        return False
      # Positive = descending, Negative = ascending
      if (ascending is None and difference != 0):
        ascending = difference < 0
      elif (ascending and difference >= 0) or ((not ascending) and difference <= 0):
        return False
    previous_report_num = report_num
  return True

def determine_safe_with_dampener(report):
  for index in range(len(report)):
    level_removed = report[:]
    del level_removed[index]
    if determine_report_safety(level_removed):
      return True
  return False

reports = parse_input_file()
no_bad_level_reports = 0
dampened_safe_reports = 0
for report in reports:
  if (determine_report_safety(report)):
    no_bad_level_reports += 1
  elif (determine_safe_with_dampener(report)):
    dampened_safe_reports += 1

print(f"Total Safe Reports: {no_bad_level_reports}")
print(f"Total Safe Reports With Dampener: {no_bad_level_reports + dampened_safe_reports}")
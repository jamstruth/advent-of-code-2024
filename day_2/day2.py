import pprint

def parse_input_file():
  with open("day2_input", "r") as input:
    lines = input.readlines()
    reports = []
    for line in lines:
      reports.append(list(map(lambda numstring: int(numstring), line.split(' '))))
    return reports
  

def determine_report_safety(report):
  ascending = None
  previous_report_num = None
  for report_num in report:
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

reports = parse_input_file()
total_safe_reports = 0
for report in reports:
  if determine_report_safety(report):
    total_safe_reports += 1

print(f"Total Safe Reports: {total_safe_reports}")
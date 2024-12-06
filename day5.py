
INPUT_FILE = 'inputs/day5_practice'

def parse_file():
  rules = []
  all_pages = []
  with open(INPUT_FILE, "r") as input:
    parsing_pages = False
    for line in input.read().splitlines(): # This method means not \ns (why are they there.)
      if line == "":
        parsing_pages = True
        continue
      if(parsing_pages):
        # Get out list of page numbers
        pages = list(map(lambda x: int(x), line.split(',')))
        all_pages.append(pages)
      else:
        # Get left and right numbers for the rule
        [left_num_str, right_num_str] = line.split('|')
        rules.append((int(left_num_str), int(right_num_str)))
  return (rules, all_pages)

def determine_pages_in_correct_order(pages, rules):
  # Find all relevant rules from list
  relevant_rules = [rule for rule in rules if any(page in rule for page in pages)]
  seen_pages = []
  for page in pages:
    if not seen_pages:
      # If we have no pages no need to check
      seen_pages.append(page)
      continue
    

(rules, all_pages) = parse_file()

for page_set in all_pages:
  determine_pages_in_correct_order(page_set, rules)
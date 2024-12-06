
INPUT_FILE = 'inputs/day5_input'

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
  result = True
  for index, page in enumerate(pages):
    relevant_rules = [rule for rule in rules if page in rule]
    after_pages = []
    before_pages = []
    for (before_page, after_page) in relevant_rules:
      # Split into before and after lists
      if before_page == page:
        # The after page must be after it somewhere and not before
        before_pages.append(after_page)
      if after_page == page:
        # These before page must be before it somewhere and not after
        after_pages.append(before_page)
    # Split into pages before and after our current page
    pages_before = set(pages[:index])
    pages_after = set(pages[index+1:])
    # If pages before does not contain any of the pages we must be before
    # and if pages after does not contain any of the pages we must be before
    # then we are safe on this page
    if(not(pages_before.isdisjoint(before_pages) and pages_after.isdisjoint(after_pages))):
      print(f"Pages: {pages} is not valid!")
      result = False
      break # Early jump out of loop. Once its the wrong order, no need to go further
  return result

(rules, all_pages) = parse_file()
total_middle_numbers = 0
for page_set in all_pages:
  result = determine_pages_in_correct_order(page_set, rules)
  if result:
    # Determine middle index
    print(f"Valid Pageset {page_set}, Middle Number: {page_set[int((len(page_set)-1)/2)]}")
    total_middle_numbers += page_set[int((len(page_set)-1)/2)]

print(f"Total of Middle Number: {total_middle_numbers}")
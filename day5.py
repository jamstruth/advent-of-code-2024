
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

def determine_rules_for_page(page, rules):
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
  return (after_pages, before_pages)

def determine_page_set_in_correct_order(page_set, rules):
  # Find all relevant rules from list
  result = True
  for index, page in enumerate(page_set):
    (after_pages, before_pages) = determine_rules_for_page(page, rules)
    # Split into pages before and after our current page
    pages_before = set(page_set[:index])
    pages_after = set(page_set[index+1:])
    # If pages before does not contain any of the pages we must be before
    # and if pages after does not contain any of the pages we must be before
    # then we are safe on this page
    if(not(pages_before.isdisjoint(before_pages) and pages_after.isdisjoint(after_pages))):
      result = False
      break # Early jump out of loop. Once its the wrong order, no need to go further
  return result

def correct_page_set_order(page_set, rules):
  new_page_set = page_set[:]
  print(f"Original Set: {new_page_set}")
  for page in page_set:
    new_page_set = reorder_set_for_rules(new_page_set, page, rules)
    print(new_page_set)
  return new_page_set

def reorder_set_for_rules(page_set, page, rules):
  index = page_set.index(page)
  (after_pages, before_pages) = determine_rules_for_page(page, rules)
  # Split into pages before and after our current page
  pages_before = page_set[:index]
  pages_after = page_set[index+1:]
  print(f"Pages Before:{pages_before} {page} Pages After: {pages_after}")
  new_pages_before = []
  new_pages_after = []
  for before_page in pages_before:
    if(before_page in before_pages):
      new_pages_after.append(before_page)
    else:
      new_pages_before.append(before_page)
  for after_page in pages_after:
    if(after_page in after_pages):
      new_pages_before.append(after_page)
    else:
      new_pages_after.append(after_page)
  return new_pages_before + [page] + new_pages_after

(rules, all_pages) = parse_file()
total_middle_numbers = 0
total_corrected_middle_numbers = 0
for page_set in all_pages:
  valid_order = determine_page_set_in_correct_order(page_set, rules)
  if valid_order:
    # Determine middle index
    total_middle_numbers += page_set[int((len(page_set)-1)/2)]
  else:
    new_page_set = correct_page_set_order(page_set, rules)
    print(f"Corrected {page_set} to {new_page_set}")
    print(f"This new set's validity is {determine_page_set_in_correct_order(new_page_set, rules)}")
    total_corrected_middle_numbers += new_page_set[int((len(new_page_set)-1)/2)]

print(f"Total of Middle Number for correctly ordered sets: {total_middle_numbers}")
print(f"Total of Middle Numbers with corrected sets: {total_corrected_middle_numbers}")
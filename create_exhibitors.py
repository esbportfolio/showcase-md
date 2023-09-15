"""Create text files with exhibitor data for Map Dynamics"""

## IMPORTS ##

# External packages
import csv

## CONSTANT ##

IMPORT_FILE = 'C:/Users/elizabeth/Documents/Local Code/Showcase MD Tool/Export MD Exhibitors.csv'
EXPORT_FILE = 'exhibitors.txt'

## FUNCTIONS ##

def add_new_lines(input_text, num_lines):
    return input_text + '\n' * num_lines

def co_text(co_dict):
    """
    Generates text for each exhibitor, returns a string

    Parameters
    ----------
    co_dict : dict
        Dictionary of data about the exhibiting company
    """
    # Main profile page
    co_text = add_new_lines('--MAIN PROFILE--', 1)
    co_text += add_new_lines(co_dict['Attendee Company'], 1)
    if int(co_dict['Hide License']) == 0:
        co_text += '* ' + co_dict['License'] + ' '
    co_text += add_new_lines('* ' + co_dict['Member_Since'], 2)
    # Contact page
    co_text += add_new_lines('--CONTACT US--', 1)
    co_text += add_new_lines(co_dict['Addr1'], 1)
    co_text += add_new_lines(co_dict['City'], 1)
    co_text += add_new_lines(co_dict['State/Province'], 1)
    co_text += add_new_lines(co_dict['Postal Code'], 1)
    if int(co_dict['Exclude Contact']) == 0:
        co_text += add_new_lines(co_dict['Public Contact First'], 1)
        co_text += add_new_lines(co_dict['Public Contact Last'], 1)
    co_text += add_new_lines(co_dict['Public Contact Email'], 1)
    co_text += add_new_lines(co_dict['Phone'], 1)
    co_text += 'http://' + add_new_lines(co_dict['Website'], 2)
    # Contact form page
    co_text += add_new_lines('--CONTACT FORM--', 1)
    co_text += add_new_lines(co_dict['Public Contact Email'], 2)
    # Separator
    co_text += add_new_lines('-' * 40, 2)
    return co_text

## MAIN ##

# Read in the CSV
with open(IMPORT_FILE, newline='', encoding='utf-8') as csv_file:
    import_data = list(csv.DictReader(csv_file))
csv_file.close()

# Set up a set to hold companies
co_set = set()
# Set up an empty string to hold text
output_text = ''

# Iterate through the data
for row in import_data:
    # If the company data hasn't been created
    if row['Attendee Company'] not in co_set:
        # Write a file of company data
        output_text += co_text(row)
        # Add the company name to the set
        co_set.add(row['Attendee Company'])

with open(EXPORT_FILE, 'w') as output_file:
    output_file.write(output_text)
output_file.close()
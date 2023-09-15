"""Create text files with exhibitor data for Map Dynamics"""

## IMPORTS ##

# External packages
import csv
import re

## CONSTANT ##

IMPORT_ENTRY = 'C:/Users/elizabeth/Documents/Local Code/Showcase MD Tool/Export MD Entries.csv'
IMPORT_COORD = 'C:/Users/elizabeth/Documents/Local Code/Showcase MD Tool/Import Lat Long.csv'
EXPORT_FILE = 'entries.txt'

## FUNCTIONS ##

def add_new_lines(input_text, num_lines):
    """
    Adds new line markers

    Parameters
    ----------
    input_text : str
        Text the user wants to append to
    num_lines : int
        Number of new line markers to add
    """
    return input_text + '\n' * num_lines

# Clean up trailing zeros
def trailing_zeros(val):
    val = val.replace('.00', '')
    val = re.sub('(.[1-9])0', r'\1', val)
    return val

def entry_text(entry_dict):
    """
    Generates text for each exhibitor, returns a string

    Parameters
    ----------
    entry_dict : dict
        Dictionary of data about the exhibiting company
    """
    feat_list = ['Entry Feature 1','Entry Feature 2','Entry Feature 3','Entry Feature 4','Entry Feature 5','Entry Feature 6']
    
    # Listing info tab
    entry_text = add_new_lines('--LISTING INFORMATION--', 1)
    entry_text += add_new_lines(
        entry_dict['Entry Num'] + ' - ' + \
        entry_dict['Attendee Company'] + '<br>' + \
        entry_dict['Price'],
        2
    )
    # Description Starts
    entry_text += add_new_lines('\t--Description--', 1)
    entry_text += add_new_lines(
        '<b>' + entry_dict['Entry Street Address'] + ', ' + \
        entry_dict['Entry City'] + ' (' + \
        entry_dict['Entry Subdivision'] + ')</b>',
        1
    )
    entry_text += add_new_lines(entry_dict['Entry Type'], 2)
    # Home/townhome content
    if abs(int(entry_dict['Is_Dev'])) == 0:
        beds = trailing_zeros(entry_dict['Bedrooms'])
        baths = trailing_zeros(entry_dict['Bathrooms'])
        entry_text += add_new_lines('Bedrooms: ' + beds + ' ** Bathrooms: ' + baths, 1)
        entry_text += add_new_lines(
            'Finished Sqft: ' + entry_dict['Living SF'] + ' ** ' \
            'Total Sqft: ' + entry_dict['Total SF'] + ' ** ' + \
            'Garage Sqft: ' + entry_dict['Garage SF'],
            1
        )
        entry_text += add_new_lines(
            'Style: ' + entry_dict['Home Style'] + ' ** ' \
            'Exterior: ' + entry_dict['Exterior'],
            2
        )
    # Description
    entry_text += add_new_lines(entry_dict['Description'], 2)
    # Amenities
    feat_text = ''
    for feat in feat_list:
        if len(entry_dict[feat]) > 0:
            feat_text += u'\u2022 ' + entry_dict[feat] + ' '
    entry_text += add_new_lines(feat_text, 2)
    # Navigation
    entry_text += add_new_lines('<i>Navigation:</i>', 1)
    link_text = '<a href="' + entry_dict['Google Maps Link'] + '"><u>Click here for Google Maps link</u></a>'
    if int(entry_dict['Need Directions']) == 0:
        entry_text += add_new_lines(link_text, 1)
    else:
        entry_text += add_new_lines('This entry\'s address cannot be found directly in Google Maps.  ' + \
        'To provide easier navigation, these directions start from a location that can be found in Google Maps ' + \
        '(linked below), then provide guidance from there.', 2)
        entry_text += add_new_lines(link_text, 1)
        entry_text += add_new_lines(entry_dict['Directions'], 1)
    entry_text += add_new_lines('\t--Description--', 2)
    # Location info tab
    entry_text += add_new_lines('--LOCATION INFORMATION--', 1)
    entry_text += add_new_lines(entry_dict['Entry Street Address'], 1)
    entry_text += add_new_lines(entry_dict['Entry City'], 1)
    entry_text += add_new_lines('MN', 1)
    entry_text += add_new_lines(entry_dict['Entry Zip'], 2)
    if int(entry_dict['Need Directions']) != 0:
        entry_text += add_new_lines(coord_dict[entry_dict['Entry Num']]['lat'], 1)
        entry_text += add_new_lines(coord_dict[entry_dict['Entry Num']]['long'], 2)
    # Location info tab
    entry_text += add_new_lines('--RELATED EXHIBITORS--', 1)
    entry_text += add_new_lines(entry_dict['Attendee Company'], 1)
    if int(entry_dict['Is_Dev']) == 0:
        entry_text += add_new_lines('Builder', 2)
    else:
        entry_text += add_new_lines('Developer', 2)
    # Separator
    entry_text += add_new_lines('-' * 40, 2)
    return entry_text

## MAIN ##

# Read in the entry CSV
with open(IMPORT_ENTRY, newline='') as csv_file:
    import_data = list(csv.DictReader(csv_file))
csv_file.close()

# Get a set of entries that need latitudes and longitudes
coord_set = set( \
    [row['Entry Num'] \
    for row in import_data \
    if abs(int(row['Need Directions'])) == 1]
)

# Read in the coordinate CSV
with open(IMPORT_COORD, newline='') as csv_file:
    # Create an empty dictionary
    coord_dict = {}
    # Read the CSV
    reader = csv.DictReader(csv_file)
    for row in reader:
        # If this entry is in the set created above (meaning it needs lat/long)
        if row['Entry Num'] in coord_set:
            # Create a dictionary that stores the entry number as the key and 
            # a nested dictionary with lat/long values
            coord_dict[row['Entry Num']] = {
                'lat' : row['Lat'],
                'long' : row['Long']
            }
csv_file.close()

# Set up an empty string to hold text
output_text = ''

# Iterate through the data
for row in import_data:
    output_text += entry_text(row)

with open(EXPORT_FILE, 'w') as output_file:
    output_file.write(output_text)
output_file.close()
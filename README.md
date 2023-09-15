# Showcase Data Tool
This is a tool I created to help automate the process of turning registrations into a Word document for our in-house designer.
## Packages Used
* csv
* re
## Project Goals
### create_entries
1. Pull in data about entries from a CSV.
2. Format it as a text file with information for each entry, to make entry into MapDynamics easier.
    * Document should exclude fields not relevent for entry type (e.g. a development should not have a spot for bedrooms/bathrooms).
    * For bulleted list of features, document should only include as many bullet items as there are features provided (number of features can vary between entries).
3. Save document with correct naming convention.
### create_exhibitors
1. Pull in data about unique participating companies from a CSV.
2. Format it as a text file with information for each entry, to make entry into MapDynamics easier.
    * Document should exclude fields not present (such as a contact name is none was provided).
3. Save document with correct naming convention.
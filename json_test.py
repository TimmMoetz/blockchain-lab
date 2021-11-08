import json
# Create a JSON Object
json_obj = {}
json_obj['employees'] = []
json_obj['employees'].append({
    'emp_name': 'John Watson',
    'date_of_join': '01-01-2015'
})
# Write the object to file.
with open('example.json', 'w') as jsonFile:
    json.dump(json_obj, jsonFile)

import os
import json

file_path = os.path.join(os.getcwd(), 'chemical_composition.json')
with open(file_path, 'r') as file_object:
    chemical_composition_data = json.load(file_object)

count = 0
for k, v in chemical_composition_data.items():
    count += 1
    string = k.replace('~', ' ')
    print(f'{string}: {v}')

    if not count % 10:
        answer = input('\t\t\t\t\t\tType "X" to break. Any key to continue.')
        if answer.upper() == 'X':
            break

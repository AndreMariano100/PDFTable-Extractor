import os
import json

# Reads the chemical composition data
file_path = os.path.join(os.getcwd(), 'a_chemical_composition.json')
with open(file_path, 'r') as file_object:
    chemical_composition_data = json.load(file_object)

thermal_expansion_grouping = {}

thermal_expansion_groups = {
    'Group 1': ('Carbon steel', 'C–Mn–Cb', 'C–Mn–Si–Cb', 'C–Mn–Si–V', 'C–Mn–Ti', 'C–Si–Ti', 'C–1/4Mo', 'C–1/2Mo',
                '1/2Cr–1/5Mo', '1/2Cr–1/5Mo–V', '1/2Cr–1/4Mo–Si', '1/2Cr–1/2Mo', '3/4Cr–1/2Ni–Cu', '3/4Cr–3/4Ni–Cu–Al',
                '1Cr–1/5Mo', '1Cr–1/5Mo–Si', '1Cr–1/2Mo', '1Cr–1/2Mo–V', '1 1/4Cr–1/2Mo', '1 1/4Cr–1/2Mo–Si',
                '1 3/4Cr–1/2Mo–Cu', '1 3/4Cr–1/2Mo–Ti', '2Cr–1/2Mo', '2 1/4Cr–1Mo', '3Cr–1Mo', '3Cr–1Mo–1/4V–Cb–Ca',
                '3Cr–1Mo–1/4V–Ti–B', 'Mn–1/4Mo', 'Mn–1/2Mo', 'Mn–1/2Mo–1/4Ni', 'Mn–1/2Mo–1/2Ni', 'Mn–1/2Mo–3/4Ni',
                'Mn–V', '1/2Ni–1/2Cr–1/4Mo', '1/2Ni–1/2Cr–1/4Mo–V', '1/2Ni–1/2Mo–V', '3/4Ni–1/2Cr–1/2Mo–V',
                '3/4Ni–1/2Cu–Mo', '3/4Ni–1/2Mo–1/3Cr–V', '3/4Ni–1/2Mo–Cr–V', '3/4Ni–1Mo–3/4Cr', '1Ni–1/2Cr–1/2Mo',
                '1 1/4Ni–1Cr–1/2Mo', '1 3/4Ni–3/4Cr–1/4Mo', '2Ni–3/4Cr–1/4Mo', '2Ni–3/4Cr–1/3Mo', '2Ni–11/2Cr–1/4Mo–V',
                '2 1/2Ni', '2 3/4Ni–1 1/2Cr–1/2Mo–V', '3 1/2Ni', '3 1/2Ni–1 3/4Cr–1/2Mo–V', '4Ni–1 1/2Cr–1/2Mo–V'),
    'Group 2': ('18Cr–5Ni–3Mo–N', '22Cr–2Ni–Mo–N', '22Cr–5Ni–3Mo–N', '23Cr–4Ni–Mo–Cu', '25Cr–7Ni–4Mo–N',
                '25Cr–6Ni–Mo–N'),
    'Group 3': ('16Cr–12Ni–2Mo', '16Cr–12Ni–2Mo–N', '16Cr–12Ni–2Mo–Ti', '18Cr–8Ni', '18Cr–8Ni–N', '18Cr–10Ni–Cb',
                '18Cr–10Ni–Ti', '18Cr–11Ni', '18Cr–13Ni–3Mo', '18Cr–15Ni–4Si', '18Cr–18Ni–2Si', '19Cr–9Ni–Mo–W',
                '21Cr–11Ni–N'),
    'Group 4': ('14Cr–16Ni–6Si–Cu–Mo', '25Ni–15Cr–2Ti', '29Ni–20Cr–3Cu–2Mo', '18Cr–20Ni–5.5Si', '20Cr–18Ni–6Mo',
                '22Cr–13Ni–5Mn', '23Cr–12Ni', '24Cr–22Ni–6Mo–2W–Cu–N', '25Cr–12Ni', '25Cr–20Ni', '25Cr–20Ni–2Mo',
                '31Ni–31Fe–29Cr–Mo', '44Fe–25Ni–21Cr–Mo', '47Fe–25Ni–23Cr–5.5Mo–N'),
    'Specific': ('5Cr–1Mo', '29Cr–7Ni–2Mo–N', '9Cr–1Mo', '5Ni–1/4Mo', '7% Nickel Steel', '8Ni', '9Ni',
                 '12Cr', '12Cr–1Al', '13Cr', '13Cr–4Ni', '15Cr', '17Cr', '27Cr', 'Ductile cast iron',
                 '17Cr–4Ni–4Cu')

}
no_group = {
    '...': 'no group',
    'C–Mn–Si–V–Cb': 'no group',
    'C–0.3Mo': 'no group',
    'Mn–1/4Mo–V': 'no group',
    'Mn–1/2Ni–V': 'no group',

    '1 1/2Si–1/2Mo': 'no group',

    '3/4Cr': 'no group',
    '1Cr–V': 'no group',
    '1Cr–1/4Si–V': 'no group',
    '1Cr–1Mn–1/4Mo': 'no group',
    '2 1/4Cr–1Mo–V': 'no group',
    '5Cr–1/2Mo': 'no group',
    '5Cr–1/2Mo–Si': 'no group',
    '5Cr–1/2Mo–Ti': 'no group',
    '9Cr–1Mo–V': 'no group',

    '12Cr–1Mo–V–W': 'no group',
    '11Cr–Ti': 'no group',
    '12Cr–Al': 'no group',
    '12Cr–Ti': 'no group',
    '12 1/2Cr–2Ni': 'no group',
    '12Cr–9Ni–2Cu–1Ti': 'no group',
    '13Cr–8Ni–2Mo': 'no group',
    '15Cr–5Ni–3Cu': 'no group',
    '15Cr–6Ni–Cu–Mo': 'no group',
    '16Cr–4Ni–6Mn': 'no group',
    '16Cr–9Mn–2Ni–N': 'no group',
    '16Cr–12Ni–2Mo–Cb': 'no group',
    '17Cr–4Ni–6Mn': 'no group',
    '17Cr–4Ni–3Cu': 'no group',
    '17Cr–7Ni': 'no group',
    '17.5Cr–17.5Ni–5.3Si': 'no group',
    '17Cr–7Ni–1Al': 'no group',
    '18Cr–2Mo': 'no group',
    '18Cr–Ti': 'no group',
    '18Cr–3Ni–12Mn': 'no group',
    '18Cr–5Ni–3Mo': 'no group',
    '18Cr–8Ni–Se': 'no group',
    '18Cr–8Ni–4Si–N': 'no group',
    '18Cr–9Ni–3Cu–Cb–N': 'no group',
    '19Cr–9Ni–1/2Mo': 'no group',
    '19Cr–9Ni–2Mo': 'no group',
    '19Cr–10Ni–3Mo': 'no group',
    '19Cr–15Ni–4Mo': 'no group',
    '20Cr–3Ni–1.5Mo–N': 'no group',
    '20Cr–10Ni': 'no group',
    '21Cr–5Mn–1.5Ni–Cu–N': 'no group',
    '21Cr–6Ni–9Mn': 'no group',
    '23Cr–4Ni–Mo–Cu–N': 'no group',
    '23Cr–12Ni–Cb': 'no group',
    '23Cr–25Ni–5.5Mo–N': 'no group',
    '24Cr–10Ni–4Mo–N': 'no group',
    '25Cr–4Ni–4Mo–Ti': 'no group',
    '25Cr–5Ni–3Mo–2Cu': 'no group',
    '25Cr–6.5Ni–3Mo–N': 'no group',
    '25Cr–7Ni–3Mo–W–Cu–N': 'no group',
    '25Cr–7.5Ni–3.5Mo–N–Cu–W': 'no group',
    '25Cr–20Ni–Cb': 'no group',
    '25Cr–20Ni–Cb–N': 'no group',
    '25Cr–22Ni–2Mo–N': 'no group',
    '26Cr–4Ni–Mo': 'no group',
    '26Cr–4Ni–Mo–N': 'no group',
    '26Cr–3Ni–3Mo': 'no group',
    'Co–26Cr–9Ni–5Mo–3Fe–2W': 'no group',
    '27Cr–1Mo': 'no group',
    '27Cr–1Mo–Ti': 'no group',
    '29Cr–6.5Ni–2Mo–N': 'no group',
    '29Cr–4Mo': 'no group',
    '29Cr–4Mo–2Ni': 'no group',
    '29Cr–4Mo–Ti': 'no group',
    '33Cr–31Ni–32Fe–1.5Mo–0.6Cu–N': 'no group',

    'AlSil2Fe': 'no group',

    '99Ni': 'no group',
    '99Ni–Low C': 'no group',
    '72Ni–15Cr–8Fe': 'no group',
    '70Ni–16Cr–7Fe–Ti–Al': 'no group',
    '70Ni–16Mo–7Cr–5Fe': 'no group',
    '67Ni–30Cu': 'no group',
    '67Ni–30Cu–S': 'no group',
    '67Ni–28Cu–3Al': 'no group',
    '65Ni–28Mo–2Fe': 'no group',
    '65Ni–29.5Mo–2Fe–2Cr': 'no group',
    '62Ni–22Mo–15Cr': 'no group',
    '62Ni–25Mo–8Cr–2Fe': 'no group',
    '62Ni–28Mo–5Fe': 'no group',
    '61Ni–16Mo–16Cr': 'no group',
    '60Ni–25Cr–9.5Fe–2.1Al': 'no group',
    '60Ni–23Cr–Fe': 'no group',
    '60Ni–22Cr–9Mo–3.5Cb': 'no group',
    '60Ni–19Cr–19Mo–1.8Ta': 'no group',
    '59Ni–23Cr–16Mo': 'no group',
    '59Ni–23Cr–16Mo–1.6Cu': 'no group',
    '59Ni–22Cr–14Mo–4Fe–3W': 'no group',
    '58Ni–33Cr–8Mo': 'no group',
    '58Ni–29Cr–9Fe': 'no group',
    '57Ni–22Cr–14W–2Mo–La': 'no group',
    '55Ni–21Cr–13.5Mo': 'no group',
    '54Ni–16Mo–15Cr': 'no group',
    '53Ni–17Mo–16Cr–6Fe–5W': 'no group',
    '53Ni–19Cr–19Fe–Cb–Mo': 'no group',
    '52Ni–22Cr–13Co–9Mo': 'no group',
    '49Ni–25Cr–18Fe–6Mo': 'no group',
    '47Ni–22Cr–9Mo–18Fe': 'no group',
    '47Ni–22Cr–19Fe–6Mo': 'no group',
    '47Ni–22Cr–20Fe–7Mo': 'no group',
    '46Ni–27Cr–23Fe–2.75Si': 'no group',
    '42Ni–21.5Cr–3Mo–2.3Cu': 'no group',
    '40Ni–29Cr–15Fe–5Mo': 'no group',
    '37Ni–33Fe–23Cr–4Mo–Cu': 'no group',
    '37Ni–30Co–28Cr–2.7Si': 'no group',
    '37Ni–33Fe–25Cr': 'no group',
    '35Ni–35Fe–20Cr–Cb': 'no group',
    '35Ni–30Fe–24Cr–6Mo–Cu': 'no group',
    '35Ni–23Cr–7.5Mo–N': 'no group',
    '35Ni–19Cr–1 1/4Si': 'no group',
    '33Ni–42Fe–21Cr': 'no group',
    '42Fe–33Ni–21Cr': 'no group',
    '32Ni–45Fe–20Cr–Cb': 'no group',
    '32Ni–44Fe–21Cr': 'no group',
    '31Ni–33Fe–27Cr–6.5Mo–Cu–N': 'no group',
    '27Ni–22Cr–7Mo–Mn–Cu–N': 'no group',
    '26Ni–43Fe–22Cr–5Mo': 'no group',
    '25Ni–47Fe–21Cr–5Mo': 'no group',
    '25Ni–20Cr–6Mo–Cu–N': 'no group',
    '46Fe–24Ni–21Cr–6Mo–N': 'no group',
    '21Ni–30Fe–22Cr–18Co–3Mo–3W': 'no group',

    '7Ni': 'no group',
    '3Ni–1 3/4Cr–1/2Mo': 'no group',
    '2 3/4Ni–1 1/2Cr–1/2Mo': 'no group',
    '2Ni–3/4Cr–1/3Mo–V': 'no group',
    '2Ni–1Cu': 'no group',
    '2Ni–1 1/2Cr–1/4Mo–V': 'no group',
    '1 1/2Ni': 'no group',
    'Ni–28Mo–3Fe–1.3Cr–0.25Al': 'no group',
    'Ni–Cr–Mo–W': 'no group',
    '3/4Ni–1Cu–3/4Cr': 'no group',

    'Ti': 'no group',
    'Ti–Pd': 'no group',
    'Ti–Ru': 'no group',
    'Ti–0.15Pd': 'no group',
    'Ti–0.05Pd': 'no group',
    'Ti–0.10Ru': 'no group',
    'Ti–0.3Mo–0.8Ni': 'no group',
    'Ti–4Al–2.5V–1.5Fe': 'no group',
    'Ti–3Al–2.5V': 'no group',
    'Ti–3Al–2.5V–0.1Ru': 'no group',

    '99.2Zr': 'no group',
    '95.5Zr + 2.5Nb': 'no group'}

user_created_relation = {}

for spec, chem in chemical_composition_data.items():

    # Tries to find the chemical composition in the material grouping
    found = False
    group = ''
    for k, v in thermal_expansion_groups.items():
        if chem in v:
            found = True
            group = k
            break

    # If found, saves it to the dictionary
    if found:
        thermal_expansion_grouping[spec] = group

    # Else, shows it
    else:
        if chem in user_created_relation:
            continue

        # print(f'{spec}: {chem} \tNot found')
        # group = input('Enter group name: ')
        user_created_relation[chem] = 'no group'

        # print(user_created_relation)

# Writes the thermal expansion grouping data
file_path = os.path.join(os.getcwd(), 'b_thermal_expansion_group.json')
with open(file_path, 'w') as file_object:
    json.dump(thermal_expansion_grouping, file_object)

print('Thermal Expansion Grouping')
print(thermal_expansion_grouping)

print('User created thermal group relatio')
print(user_created_relation)

print(list(no_group.keys()))


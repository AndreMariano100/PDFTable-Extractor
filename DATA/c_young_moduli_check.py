import os
import json

# Reads the chemical composition data
file_path = os.path.join(os.getcwd(), 'a_chemical_composition.json')
with open(file_path, 'r') as file_object:
    chemical_composition_data = json.load(file_object)

elastic_moduli_grouping = {}
no_group = {}

# ----------------------------------------------------------------------------------------------------------------------

elasticity_moduli_groups = {
    'Carbon Steel with C ≤ 0.30%': ('Carbon steel',),
    'Ductile cast iron': ('Ductile cast iron',),
    'Group A': ('C–1/4Mo', 'C–1/2Mo', 'Mn–1/4Mo', 'Mn–1/2Mo', 'Mn–1/2Mo–1/4Ni', 'Mn–1/2Mo–1/2Ni', 'Mn–1/2Ni–V', 'Mn–V'),
    'Group B': ('3/4Cr–1/2Ni–Cu', '3/4Cr–3/4Ni–Cu–Al', '1/2Ni–1/2Cr–1/4Mo–V', '1/2Ni–1/2Mo–V', '3/4Ni–1/2Cr–1/2Mo–V',
                '3/4Ni–1/2Cu–Mo', '3/4Ni–1/2Mo–1/3Cr–V', '3/4Ni–1/2Mo–Cr–V', '3/4Ni–1Mo–3/4Cr', '1Ni–1/2Cr–1/2Mo',
                '1 1/4Ni–1Cr–1/2Mo', '1 3/4Ni–3/4Cr–1/4Mo', '2Ni–11/2Cr–1/4Mo–V', '2Ni–1Cu', '2 1/2Ni',
                '2 3/4Ni–1 1/2Cr–1/2Mo–V', '3 1/2Ni', '3 1/2Ni–1 3/4Cr–1/2Mo–V', '4Ni–1 1/2Cr–1/2Mo–V', '7Ni'),
    'Group C': ('1/2Cr–1/5Mo–V', '1/2Cr–1/4Mo–Si', '1/2Cr–1/2Mo', '1Cr–1/5Mo', '1Cr–1/2Mo',
                '1Cr–1/2Mo–V', '1 1/4Cr–1/2Mo', '1 1/4Cr–1/2Mo–Si', '1 3/4Cr–1/2Mo–Ti', '2Cr–1/2Mo'),
    'Group D': ('2 1/4Cr–1Mo', '3Cr–1Mo', '3Cr–1Mo–1/4V–Cb–Ca', '3Cr–1Mo–1/4V–Ti–B'),
    'Group E': ('5Cr–1/2Mo', '5Cr–1/2Mo–Si', '5Cr–1/2Mo–Ti', '7Cr–1/2Mo', '9Cr–Mo', '9Cr–1Mo', '9Cr–1Mo–V'),
    'Group F': ('12Cr–Al', '13Cr', '15Cr', '17Cr'),
    'Group G': ('16Cr–12Ni–2Mo', '16Cr–12Ni–2Mo–N', '18Cr–3Ni–13Mn', '18Cr–8Ni', '18Cr–8Ni–N', '18Cr–8Ni–S',
                '18Cr–8Ni–Se', '18Cr–10Ni–Cb', '18Cr–10Ni–Ti', '18Cr–13Ni–3Mo', '18Cr–18Ni–2Si', '21Cr–6Ni–9Mn',
                '22Cr–13Ni–5Mn', '23Cr–12Ni', '25Cr–20Ni'),
    'Group H': ('18Cr–5Ni–3Mo', '22Cr–2Ni–Mo–N', '22Cr–5Ni–3Mo–N', '23Cr–4Ni–Mo–Cu–N', '24Cr–10Ni–4Mo–N',
                '25Cr–5Ni–3Mo–2Cu', '25Cr–6Ni–Mo–N', '25Cr–6.5Ni–3Mo–N', '25Cr–7Ni–3Mo–W–Cu–N', '25Cr–7Ni–4Mo–N',
                '25Cr–7.5Ni–3.5Mo–N–Cu–W', '29Cr–6.5Ni–2Mo–N'),
    'Group I': ('14Cr–16Ni–6Si–Cu–Mo', '17.5Cr–17.5Ni–5.3Si', '18Cr–8Ni–4Si–N', '18Cr–20Ni–5.5Si'),
    'Group J': ('27Ni–22Cr–7Mo–Cu–N', '20Cr–18Ni–6Mo', '24Cr–22Ni–6Mo–2W–Cu–N', '31Ni–31Fe–29Cr–Mo',
                '46Fe–24Ni–21Cr–6Mo–N', '25Ni–47Fe–21Cr–5Mo', '25Ni–47Fe–23Cr–5.5Mo–N', '44Fe–25Ni–21Cr–Mo',
                '25Ni–20Cr–6Mo–Cu–N'),
    'Group 11': ('13Cr–8Ni–2Mo', 'XM‐13', 'PH13‐8Mo.'),
    'Group 12': ('15Cr–5Ni–3Mo', 'XM‐12', '15‐5PH'),
    'Group 13': ('15Cr–6Ni–Cu–Mo', 'Custom 450', 'XM‐25'),
    'Group 14': ('17Cr–4Ni–4Cu Grade 630', '17‐4PH'),
    'Group 15': ('17Cr–7Ni–1Al Grade 631', '17‐7PH'),
    'Group 16': ('25Ni–15Cr–2Ti Grade 660', 'A‐286 stainless steel'),

}

for spec, chem in chemical_composition_data.items():

    # Tries to find the chemical composition in the material grouping
    found = False
    group = ''
    for k, v in elasticity_moduli_groups.items():
        if chem in v:
            found = True
            group = k
            break

    # If found, saves it to the dictionary
    if found:
        elastic_moduli_grouping[spec] = group

    # Else, saves on the no group dict
    else:
        no_group[chem] = 'no group'


# Writes the thermal expansion grouping data
file_path = os.path.join(os.getcwd(), 'c_young_moduli_group.json')
with open(file_path, 'w') as file_object:
    json.dump(elastic_moduli_grouping, file_object)

print('Elastic Moduli Grouping')
print(elastic_moduli_grouping)

print('No group')
print(list(no_group.keys()))

"""
Unsuccesfull grouping
['Carbon steel', 'Ductile cast iron', 
 'C–Mn–Si–Cb', 'C–Mn–Si–V', 'C–Mn–Si–V–Cb', 'C–Mn–Ti', 'C–Si–Ti', 'C–0.3Mo', 
 '1 1/2Si–1/2Mo', 'Mn–1/4Mo–V', 'Mn–1/2Mo–3/4Ni', '...', 
 
 '1/2Cr–1/5Mo', '1Cr–1/4Si–V', '1Cr–V', '1 3/4Cr–1/2Mo–Cu', '2 1/4Cr–1Mo–V', 
 '3/4Cr', '1Cr–1Mn–1/4Mo',
 
 '11Cr–Ti', '12Cr', '12Cr–Ti', '12Cr–1Mo–V–W', '12Cr–9Ni–2Cu–1Ti', '12 1/2Cr–2Ni','13Cr–4Ni', 
 '15Cr–5Ni–3Cu', '16Cr–4Ni–6Mn', '16Cr–9Mn–2Ni–N', '16Cr–12Ni–2Mo–Cb', '16Cr–12Ni–2Mo–Ti', '17Cr–4Ni–6Mn', '17Cr–7Ni', 
 '17Cr–4Ni–4Cu', '17Cr–7Ni–1Al', '17Cr–4Ni–3Cu', '18Cr–15Ni–4Si', '18Cr–2Mo','18Cr–Ti', '18Cr–3Ni–12Mn', 
 '18Cr–9Ni–3Cu–Cb–N', '18Cr–11Ni', '19Cr–9Ni–1/2Mo', '19Cr–9Ni–Mo–W', '19Cr–9Ni–2Mo', '19Cr–10Ni–3Mo', '19Cr–15Ni–4Mo',
 
 '20Cr–3Ni–1.5Mo–N', '20Cr–10Ni', '21Cr–5Mn–1.5Ni–Cu–N', '21Cr–11Ni–N', 
 '23Cr–12Ni–Cb', '23Cr–25Ni–5.5Mo–N', '25Cr–4Ni–4Mo–Ti', '25Cr–12Ni', '25Cr–20Ni–Cb', '25Cr–20Ni–Cb–N', 
 '25Cr–22Ni–2Mo–N', '26Cr–4Ni–Mo','26Cr–4Ni–Mo–N',
 '26Cr–3Ni–3Mo', '27Cr', '27Cr–1Mo', '27Cr–1Mo–Ti', '29Cr–4Mo', '29Cr–4Mo–2Ni', '29Cr–4Mo–Ti', 
 
 '1 1/2Ni', '1/2Ni–1/2Cr–1/4Mo', '3/4Ni–1Cu–3/4Cr', '2Ni–3/4Cr–1/3Mo–V',
 '2Ni–3/4Cr–1/4Mo', '2Ni–3/4Cr–1/3Mo', '2Ni–1 1/2Cr–1/4Mo–V', '2 3/4Ni–1 1/2Cr–1/2Mo', 
 '3Ni–1 3/4Cr–1/2Mo', '5Ni–1/4Mo', '8Ni', '9Ni', 
 
 '25Ni–15Cr–2Ti', '27Ni–22Cr–7Mo–Mn–Cu–N', '29Ni–20Cr–3Cu–2Mo', 
  
 '99Ni', '99Ni–Low C', '67Ni–30Cu', '67Ni–30Cu–S', '67Ni–28Cu–3Al', '47Ni–22Cr–9Mo–18Fe', '47Ni–22Cr–19Fe–6Mo', 
 '55Ni–21Cr–13.5Mo', '60Ni–25Cr–9.5Fe–2.1Al', '40Ni–29Cr–15Fe–5Mo', '58Ni–33Cr–8Mo', '46Ni–27Cr–23Fe–2.75Si', 
  '59Ni–23Cr–16Mo',  '59Ni–23Cr–16Mo–1.6Cu', '60Ni–19Cr–19Mo–1.8Ta', '57Ni–22Cr–14W–2Mo–La', '61Ni–16Mo–16Cr', 
  '72Ni–15Cr–8Fe', '60Ni–23Cr–Fe', '52Ni–22Cr–13Co–9Mo', 
 '60Ni–22Cr–9Mo–3.5Cb', 'Ni–Cr–Mo–W', '58Ni–29Cr–9Fe', '49Ni–25Cr–18Fe–6Mo', '47Ni–22Cr–20Fe–7Mo', 
 '35Ni–35Fe–20Cr–Cb', '37Ni–33Fe–23Cr–4Mo–Cu', '35Ni–30Fe–24Cr–6Mo–Cu', '31Ni–33Fe–27Cr–6.5Mo–Cu–N', 
 '37Ni–33Fe–25Cr', '26Ni–43Fe–22Cr–5Mo', '35Ni–19Cr–1 1/4Si', '35Ni–23Cr–7.5Mo–N', '32Ni–45Fe–20Cr–Cb', 
 '33Ni–42Fe–21Cr', '32Ni–44Fe–21Cr', '42Ni–21.5Cr–3Mo–2.3Cu', '62Ni–28Mo–5Fe', '70Ni–16Mo–7Cr–5Fe', '62Ni–25Mo–8Cr–2Fe',
  '54Ni–16Mo–15Cr', '62Ni–22Mo–15Cr', 'Ni–28Mo–3Fe–1.3Cr–0.25Al', '65Ni–28Mo–2Fe', '65Ni–29.5Mo–2Fe–2Cr', 
  '37Ni–30Co–28Cr–2.7Si', '33Cr–31Ni–32Fe–1.5Mo–0.6Cu–N', '21Ni–30Fe–22Cr–18Co–3Mo–3W', 
  59Ni–22Cr–14Mo–4Fe–3W', '53Ni–17Mo–16Cr–6Fe–5W',   '42Fe–33Ni–21Cr',   '53Ni–19Cr–19Fe–Cb–Mo', '70Ni–16Cr–7Fe–Ti–Al',
  
  'Co–26Cr–9Ni–5Mo–3Fe–2W', 
  
  'Ti', 'Ti–Pd', 'Ti–Ru', 'Ti–0.15Pd', 'Ti–0.05Pd', 'Ti–0.10Ru', 'Ti–0.3Mo–0.8Ni', 'Ti–4Al–2.5V–1.5Fe', 
  'Ti–3Al–2.5V', 'Ti–3Al–2.5V–0.1Ru', 
  
  '99.2Zr', '95.5Zr + 2.5Nb',

  'AlSil2Fe', 
"""


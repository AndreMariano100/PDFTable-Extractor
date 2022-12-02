import os
import json

# Reads the chemical composition data
file_path = os.path.join(os.getcwd(), 'chemical_composition.json')
with open(file_path, 'r') as file_object:
    chemical_composition_data = json.load(file_object)

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
                 '12Cr', '12Cr–1Al', '13Cr', '13Cr–4Ni', '15Cr', '17Cr', '27Cr', 'Ductile Cast Iron',
                 '17Cr–4Ni–4Cu')

}

all_unlisted = ['40Ni–29Cr–15Fe–5Mo', '33Ni–42Fe–21Cr', '5Cr–1/2Mo–Ti', '17Cr–7Ni–1Al', '19Cr–9Ni–1/2Mo', '35Ni–19Cr–1 1/4Si', '99.2Zr', '59Ni–23Cr–16Mo', '25Cr–20Ni–Cb', '1Cr–0.2Mo', '16Cr–9Mn–2Ni–N', '47Ni–22Cr–20Fe–7Mo', '67Ni–30Cu–S', '21Cr–6Ni–9Mn', '1 1/2Ni', '37Ni–33Fe–23Cr–4Mo–Cu', 'C–Mn–Si–V–Cb', '47Ni–22Cr–19Fe–6Mo', '59Ni–23Cr–16Mo–1.6Cu', '70Ni–16Mo–7Cr–5Fe', '3Ni–1 3/4Cr–1/2Mo', '33Cr–31Ni–32Fe–1.5Mo–0.6Cu–N', 'AlSil2Fe', '12Cr–1Mo–V–W', '32Ni–44Fe–21Cr', '18Cr–5Ni–3Mo', '35Ni–23Cr–7.5Mo–N', 'Ti–Pd', '25Cr–22Ni–2Mo–N', 'Ti–0.15Pd', '42Fe–33Ni–21Cr', 'Co–26Cr–9Ni–5Mo–3Fe–2W', '23Cr–4Ni–Mo–Cu–N', '35Ni–30Fe–24Cr–6Mo–Cu', '46Ni–27Cr–23Fe–2.75Si', '27Ni–22Cr–7Mo–Mn–Cu–N', 'C–0.3Mo', 'Ti–0.3Mo–0.8Ni', '24Cr–10Ni–4Mo–N', '17Cr–7Ni', '18Cr–Ti–Co', '26Cr–4Ni–Mo', '67Ni–30Cu', '65Ni–29.5Mo–2Fe–2Cr', '35Ni–35Fe–20Cr–Cb', '61Ni–16Mo–16Cr', '18Cr–3Ni–12Mn', '25Ni–47Fe–21Cr–5Mo', '31Ni–33Fe–27Cr–6.5Mo–Cu–N', '12Cr–Ti', '70Ni–16Cr–7Fe–Ti–Al', '99Ni', 'Ti–4Al–2.5V–1.5Fe', '57Ni–22Cr–14W–2Mo–La', '25Cr–20Ni–Cb–N', '26Ni–43Fe–22Cr–5Mo', 'Ti–0.05Pd', '3/4Ni–1Cu–3/4Cr', '25Ni–20Cr–6Mo–Cu–N', '72Ni–15Cr–8Fe', 'Ductile cast iron', 'Ti–Ru', '20Cr–10Ni', 'Ni–Cr–Mo–W', '1 3/4Ni–3/4Cr–1Mo', '19Cr–10Ni–3Mo', '1Cr–1Mn–1/4Mo', '99Ni–Low C', '23Cr–25Ni–5.5Mo–N', '37Ni–30Co–28Cr–2.7Si', '65Ni–28Mo–2Fe', '58Ni–33Cr–8Mo', 'Mn–1/2Ni–V', 'Ti', 'Ti–0.10Ru', 'Ti–3Al–2.5V', '52Ni–22Cr–13Co–9Mo', '16Cr–4Ni–6Mn', '3/4Cr', '15Cr–6Ni–Cu–Mo', 'Ti–3Al–2.5V–0.1Ru', '58Ni–29Cr–9Fe', '20Cr–3Ni–1.5Mo–N', '37Ni–33Fe–25Cr', '2Ni–1Cu', '11Cr–Ti', '1 1/2Si–1/2Mo', '46Fe–24Ni–21Cr–6Mo–N', '12Cr–Al', '62Ni–28Mo–5Fe', '25Cr–7.5Ni–3.5Mo–N–Cu–W', 'Mn–1/4Mo–V', '9Cr–1Mo–V', '15Cr–5Ni–3Cu', '17Cr–4Ni–3Cu', '5Cr–1/2Mo–Si', '23Cr–12Ni–Cb', '5Cr–1/2Mo', '19Cr–15Ni–4Mo', '60Ni–19Cr–19Mo–1.8Ta', '19Cr–9Ni–2Mo', '18Cr–Ti', '26Cr–3Ni–3Mo', '26Cr–4Ni–Mo–N', '7Ni', '60Ni–25Cr–9.5Fe–2.1Al', '21Ni–30Fe–22Cr–18Co–3Mo–3W', '25Cr–5Ni–3Mo–2Cu', '29Cr–4Mo–Ti', '42Ni–21.5Cr–3Mo–2.3Cu', '18Cr–9Ni–3Cu–Cb–N', '62Ni–25Mo–8Cr–2Fe', '27Cr–1Mo–Ti', '25Cr–7Ni–3Mo–W–Cu–N', '32Ni–45Fe–20Cr–Cb', '55Ni–21Cr–13.5Mo', '53Ni–19Cr–19Fe–Cb–Mo', '2 3/4Ni–1 1/2Cr–1/2Mo', '21Cr–5Mn–1.5Ni–Cu–N', '17.5Cr–17.5Ni–5.3Si', '2 1/4Cr–1Mo–V', '18Cr–2Mo', '1Cr–V', '54Ni–16Mo–15Cr', '60Ni–23Cr–Fe', '67Ni–28Cu–3Al', '2Ni–1 1/2Cr–1/4Mo–V', '16Cr–12Ni–2Mo–Cb', '62Ni–22Mo–15Cr', '25Cr–6.5Ni–3Mo–N', '27Cr–1Mo', '18Cr–8Ni–Se', '60Ni–22Cr–9Mo–3.5Cb', '12Cr–9Ni–2Cu–1Ti', 'Ni–28Mo–3Fe–1.3Cr–0.25Al', '29Cr–6.5Ni–2Mo–N', '13Cr–8Ni–2Mo', '29Cr–4Mo', '18Cr–8Ni–4Si–N', '29Cr–4Mo–2Ni', '1Cr–1/4Si–V', '17Cr–4Ni–6Mn', '25Cr–4Ni–4Mo–Ti', '47Ni–22Cr–9Mo–18Fe', '49Ni–25Cr–18Fe–6Mo']

# all_chem_found = []
# all_chem_not_found = []
#
# for spec, chem in chemical_composition_data.items():
#     if chem in all_chem_found:
#         continue
#
#     # print(f'{spec}: {chem}')
#     found = False
#     group = ''
#     for k, v in thermal_expansion_groups.items():
#         if chem in v:
#             found = True
#             group = k
#             break
#
#     if found:
#         # print(f'\tFound in {group}')
#         all_chem_found.append(chem)
#         # input()
#     else:
#         # print('\tNot found')
#         all_chem_not_found.append(chem)
#         # input()
#
# print(all_chem_not_found)

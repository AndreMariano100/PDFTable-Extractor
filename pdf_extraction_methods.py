import pandas as pd
import tabula
import compoundwidgets as cw


def clear_table(df):
    """ Method to clear the table from extraction artifacts: ('-', ',', '`', ' ', 'â€“', 'â‰¤') """

    for i in range(len(df)):
        for j in range(len(df.columns)):
            my_string = str(df.iloc[i, j])
            if '-' in my_string or '`' in my_string:
                my_string = my_string.replace('-', '')
                my_string = my_string.replace(' ', '')
                my_string = my_string.replace(',', '')
                my_string = my_string.replace('`', '')
                my_string = my_string.replace('â€“', '-')
                my_string = my_string.replace('â‰¤', '≤')
                df.iloc[i, j] = my_string

    return df


def adjust_chemical_composition(data_frame=None):
    """ Adjust the chemical composition read from file """

    master_translation_dict = {
        '1C– /4Mo': 'C–1/4Mo',
        'C– /4Mo': 'C–1/4Mo',
        '1C– /2Mo': 'C–1/2Mo',
        'C– /2Mo': 'C–1/2Mo',

        '1 1/2Cr– /5Mo': '1/2Cr–1/5Mo',
        '/2Cr– /5Mo': '1/2Cr–1/5Mo',
        '1 1/2Cr– /5Mo–V': '1/2Cr–1/5Mo–V',
        '/2Cr– /5Mo–V': '1/2Cr–1/5Mo–V',
        '1 1/2Cr– /4Mo–Si': '1/2Cr–1/4Mo–Si',
        '/2Cr– /4Mo–Si': '1/2Cr–1/4Mo–Si',
        '1 /2Cr– /2Mo1': '1/2Cr–1/2Mo',
        '1 1/2Cr– /2Mo': '1/2Cr–1/2Mo',
        '/2Cr– /2Mo': '1/2Cr–1/2Mo',

        '3 1/4Cr– /2Ni–Cu': '3/4Cr–1/2Ni–Cu',
        '/4Cr– /2Ni–Cu': '3/4Cr–1/2Ni–Cu',
        '3 3/4Cr– /4Ni–Cu–Al': '3/4Cr–3/4Ni–Cu–Al',
        '/4Cr– /4Ni–Cu–Al':  '3/4Cr–3/4Ni–Cu–Al',

        '11Cr– /5Mo': '1Cr–1/5Mo',
        '1Cr– /5Mo':  '1Cr–1/5Mo',
        '11Cr– /2Mo': '1Cr–1/2Mo',
        '1Cr– /2Mo': '1Cr–1/2Mo',
        '11Cr– /2Mo–V': '1Cr–1/2Mo–V',
        '1Cr– /2Mo–V': '1Cr–1/2Mo–V',
        '11Cr– /4Si–V': '1Cr–1/4Si–V',
        '1Cr–1Mn– /4Mo': '1Cr–1Mn–1/4Mo',

        '11 /4Cr– /2Mo1': '1 1/4Cr–1/2Mo',
        '1 /4Cr– /2Mo': '1 1/4Cr–1/2Mo',
        '11 /4Cr– /2Mo–Si1': '1 1/4Cr–1/2Mo–Si',
        '1 1 /4Cr– /2Mo–Si1': '1 1/4Cr–1/2Mo–Si',
        '1 /4Cr– /2Mo–Si': '1 1/4Cr–1/2Mo–Si',

        '1 /4Cr– /2Mo–Cu': '1 3/4Cr–1/2Mo–Cu',
        '11 /4Cr– /2Mo–Cu3': '1 3/4Cr–1/2Mo–Cu',
        '11 /4Cr– /2Mo–Ti3': '1 3/4Cr–1/2Mo–Ti',
        '1 /4Cr– /2Mo–Ti': '1 3/4Cr–1/2Mo–Ti',

        '12 /4Cr–1Mo': '2 1/4Cr–1Mo',
        '2 /4Cr–1Mo': '2 1/4Cr–1Mo',
        '12 /4Cr–1Mo–V': '2 1/4Cr–1Mo–V',
        '2 /4Cr–1Mo–V': '2 1/4Cr–1Mo–V',

        '13Cr–1Mo– /4V–Ti–B': '3Cr–1Mo–1/4V–Ti–B',
        '3Cr–1Mo– /4V–Ti–B': '3Cr–1Mo–1/4V–Ti–B',
        '13Cr–1Mo– /4V–Cb–Ca': '3Cr–1Mo–1/4V–Cb–Ca',
        '3Cr–1Mo– /4V–Cb–Ca': '3Cr–1Mo–1/4V–Cb–Ca',

        '15Cr– /2Mo': '5Cr–1/2Mo',
        '5Cr– /2Mo': '5Cr–1/2Mo',
        '15Cr– /2Mo–Si': '5Cr–1/2Mo–Si',
        '5Cr– /2Mo–Si': '5Cr–1/2Mo–Si',
        '15Cr– /2Mo–Ti': '5Cr–1/2Mo–Ti',
        '5Cr– /2Mo–Ti': '5Cr–1/2Mo–Ti',

        '1Mn– /4Mo': 'Mn–1/4Mo',
        'Mn– /4Mo': 'Mn–1/4Mo',
        '1Mn– /4Mo–V': 'Mn–1/4Mo–V',
        'Mn– /4Mo–V': 'Mn–1/4Mo–V',
        '1Mn– /2Mo': 'Mn–1/2Mo',
        'Mn– /2Mo': 'Mn–1/2Mo',
        '1Mn– /2Mo– /4Ni1': 'Mn–1/2Mo–1/4Ni',
        'Mn– /2Mo– /4Ni': 'Mn–1/2Mo–1/4Ni',
        '1Mn– /2Mo– /2Ni1': 'Mn–1/2Mo–1/2Ni',
        'Mn– /2Mo– /2Ni': 'Mn–1/2Mo–1/2Ni',
        '3Mn– /2Mo– /4Ni1': 'Mn–1/2Mo–3/4Ni',
        '1Mn– /2Ni–V': 'Mn–1/2Ni–V',
        'Mn– /2Ni–V': 'Mn–1/2Ni–V',

        '11 /2Si– /2Mo1': '1 1/2Si–1/2Mo',
        '1 /2Si– /2Mo': '1 1/2Si–1/2Mo',

        '1 1/2Ni– /2Cr– /4Mo–V1': '1/2Ni–1/2Cr–1/4Mo–V',
        '/2Ni– /2Cr– /4Mo–V':  '1/2Ni–1/2Cr–1/4Mo–V',
        '1 1/2Ni– /2Mo–V': '1/2Ni–1/2Mo–V',
        '/2Ni– /2Mo–V':  '1/2Ni–1/2Mo–V',

        '3 1/4Ni– /2Cr– /2Mo–V1': '3/4Ni–1/2Cr–1/2Mo–V',
        '/4Ni– /2Cr– /2Mo–V': '3/4Ni–1/2Cr–1/2Mo–V',
        '3 1/4Ni– /2Cu–Mo': '3/4Ni–1/2Cu–Mo',
        '/4Ni– /2Cu–Mo': '3/4Ni–1/2Cu–Mo',
        '3 1/4Ni– /2Mo– /3Cr–V1': '3/4Ni–1/2Mo–1/3Cr–V',
        '/4Ni– /2Mo– /3Cr–V': '3/4Ni–1/2Mo–1/3Cr–V',
        '3 1/4Ni– /2Mo–Cr–V': '3/4Ni–1/2Mo–Cr–V',
        '/4Ni– /2Mo–Cr–V': '3/4Ni–1/2Mo–Cr–V',
        '3 3/4Ni–1Mo– /4Cr': '3/4Ni–1Mo–3/4Cr',
        '/4Ni–1Mo– /4Cr': '3/4Ni–1Mo–3/4Cr',
        '/4Ni–1Cu– /4Cr': '3/4Ni–1Cu–3/4Cr',

        '11Ni– /2Cr– /2Mo1': '1Ni–1/2Cr–1/2Mo',
        '1Ni– /2Cr– /2Mo': '1Ni–1/2Cr–1/2Mo',
        '11 /4Ni–1Cr– /2Mo1': '1 1/4Ni–1Cr–1/2Mo',
        '1 /4Ni–1Cr– /2Mo': '1 1/4Ni–1Cr–1/2Mo',
        '11 /2Ni': '1 1/2Ni',
        '1 /2Ni': '1 1/2Ni',
        '11 /4Ni– /4Cr– /4Mo3 3': '1 3/4Ni–3/4Cr–1/4Mo',
        '1 /4Ni– /4Cr– /4Mo': '1 3/4Ni–3/4Cr–1/4Mo',
        '1 /4Ni– /4Cr–Mo': '1 3/4Ni–3/4Cr–1Mo',

        '12Ni– /4Cr– /4Mo3': '2Ni–3/4Cr–1/4Mo',
        '2Ni– /4Cr– /4Mo': '2Ni–3/4Cr–1/4Mo',
        '12Ni– /4Cr– /3Mo3': '2Ni–3/4Cr–1/3Mo',
        '2Ni– /4Cr– /3Mo': '2Ni–3/4Cr–1/3Mo',
        '12Ni–1 /2Cr– /4Mo–V1': '2Ni–1 1/2Cr–1/4Mo–V',
        '2Ni–1 /2Cr– /4Mo–V': '2Ni–1 1/2Cr–1/4Mo–V',

        '12 /2Ni': '2 1/2Ni',
        '2 /2Ni': '2 1/2Ni',
        '12 /4Ni–1 /2Cr– /2Mo3 1': '2 3/4Ni–1 1/2Cr–1/2Mo',
        '2 /4Ni–1 /2Cr– /2Mo': '2 3/4Ni–1 1/2Cr–1/2Mo',
        '12 /4Ni–1 /2Cr– /2Mo–V3 1': '2 3/4Ni–1 1/2Cr–1/2Mo–V',
        '2 /4Ni–1 /2Cr– /2Mo–V': '2 3/4Ni–1 1/2Cr–1/2Mo–V',

        '13Ni–1 /4Cr– /2Mo3': '3Ni–1 3/4Cr–1/2Mo',
        '3Ni–1 /4Cr– /2Mo': '3Ni–1 3/4Cr–1/2Mo',
        '13 /2Ni': '3 1/2Ni',
        '3 /2Ni': '3 1/2Ni',
        '13 /2Ni–1 /4Cr– /2Mo–V1 3': '3 1/2Ni–1 3/4Cr–1/2Mo–V',
        '3 /2Ni–1 /4Cr– /2Mo–V': '3 1/2Ni–1 3/4Cr–1/2Mo–V',
        '14Ni–1 /2Cr– /2Mo–V1': '4Ni–1 1/2Cr–1/2Mo–V',
        '4Ni–1 /2Cr– /2Mo–V': '4Ni–1 1/2Cr–1/2Mo–V',
        '15Ni– /4Mo': '5Ni–1/4Mo',
        '5Ni– /4Mo': '5Ni–1/4Mo',

        '12 /2Cr–2Ni': '12 1/2Cr–2Ni',
        '135Ni–19Cr–1 /4Si': '35Ni–19Cr–1 1/4Si',
        '35Ni–19Cr–1 /4Si': '35Ni–19Cr–1 1/4Si',
        '119Cr–9Ni– /2Mo': '19Cr–9Ni–1/2Mo',
        '19Cr–9Ni– /2Mo': '19Cr–9Ni–1/2Mo',
    }
    """untranslated_list = [
        '...', '11Cr–Ti', '12Cr', '12Cr–9Ni–2Cu–1Ti', '12Cr–Al', '12Cr–Ti', '13Cr', '13Cr–4Ni', '13Cr–8Ni–2Mo', 
        '14Cr–16Ni–6Si–Cu–Mo', '15Cr', '15Cr–5Ni–3Cu', '15Cr–6Ni–Cu–Mo', '16Cr–12Ni–2Mo', '16Cr–12Ni–2Mo–Cb', 
        '16Cr–12Ni–2Mo–N', '16Cr–12Ni–2Mo–Ti', '16Cr–4Ni–6Mn', '16Cr–9Mn–2Ni–N', '17Cr', '17Cr–4Ni–4Cu', 
        '17Cr–4Ni–6Mn', '17Cr–7Ni', '17Cr–7Ni–1Al', '18Cr–10Ni–Cb', '18Cr–10Ni–Ti', '18Cr–11Ni', '18Cr–13Ni–3Mo', 
        '18Cr–18Ni–2Si', '18Cr–2Mo', '18Cr–3Ni–12Mn', '18Cr–5Ni–3Mo', '18Cr–8Ni', '18Cr–8Ni–4Si–N', '18Cr–8Ni–N', 
        '18Cr–8Ni–Se', '18Cr–9Ni–3Cu–Cb–N', '18Cr–Ti', '19Cr–10Ni–3Mo', '19Cr–15Ni–4Mo', '19Cr–9Ni–2Mo', 
        '19Cr–9Ni–Mo–W', '1Cr–V', '20Cr–10Ni', '20Cr–18Ni–6Mo', '20Cr–3Ni–1.5Mo–N', '21Cr–11Ni–N', 
        '21Cr–5Mn–1.5Ni–Cu–N', '21Cr–6Ni–9Mn', '21Ni–30Fe–22Cr–18Co–3Mo–3W', '22Cr–13Ni–5Mn', '22Cr–5Ni–3Mo–N', 
        '23Cr–12Ni', '23Cr–12Ni–Cb', '23Cr–25Ni–5.5Mo–N', '23Cr–4Ni–Mo–Cu–N', '24Cr–10Ni–4Mo–N', 
        '24Cr–22Ni–6Mo–2W–Cu–N', '25Cr–12Ni', '25Cr–20Ni', '25Cr–20Ni–Cb', '25Cr–20Ni–Cb–N', '25Cr–22Ni–2Mo–N', 
        '25Cr–4Ni–4Mo–Ti', '25Cr–5Ni–3Mo–2Cu', '25Cr–6.5Ni–3Mo–N', '25Cr–6Ni–Mo–N', '25Cr–7.5Ni–3.5Mo–N–Cu–W', 
        '25Cr–7Ni–3Mo–W–Cu–N', '25Cr–7Ni–4Mo–N', '25Ni–15Cr–2Ti', '25Ni–20Cr–6Mo–Cu–N', '25Ni–47Fe–21Cr–5Mo', 
        '26Cr–3Ni–3Mo', '26Cr–4Ni–Mo', '26Cr–4Ni–Mo–N', '26Ni–43Fe–22Cr–5Mo', '27Cr', '27Cr–1Mo', '27Cr–1Mo–Ti', 
        '27Ni–22Cr–7Mo–Mn–Cu–N', '29Cr–4Mo', '29Cr–4Mo–2Ni', '29Cr–4Mo–Ti', '29Cr–6.5Ni–2Mo–N', '29Ni–20Cr–3Cu–2Mo', 
        '2Ni–1Cu', '31Ni–31Fe–29Cr–Mo', '31Ni–33Fe–27Cr–6.5Mo–Cu–N', '32Ni–44Fe–21Cr', '32Ni–45Fe–20Cr–Cb', 
        '33Cr–31Ni–32Fe–1.5Mo–0.6Cu–N', '33Ni–42Fe–21Cr', '35Ni–23Cr–7.5Mo–N', '35Ni–30Fe–24Cr–6Mo–Cu', 
        '35Ni–35Fe–20Cr–Cb', '37Ni–30Co–28Cr–2.7Si', '37Ni–33Fe–23Cr–4Mo–Cu', '37Ni–33Fe–25Cr', '3Cr–1Mo', 
        '40Ni–29Cr–15Fe–5Mo', '42Ni–21.5Cr–3Mo–2.3Cu', '44Fe–25Ni–21Cr–Mo', '46Fe–24Ni–21Cr–6Mo–N', 
        '46Ni–27Cr–23Fe–2.75Si', '47Ni–22Cr–19Fe–6Mo', '47Ni–22Cr–20Fe–7Mo', '47Ni–22Cr–9Mo–18Fe', '49Ni–25Cr–18Fe–6Mo',
        '52Ni–22Cr–13Co–9Mo', '54Ni–16Mo–15Cr', '55Ni–21Cr–13.5Mo', '57Ni–22Cr–14W–2Mo–La', '58Ni–29Cr–9Fe', 
        '58Ni–33Cr–8Mo', '59Ni–23Cr–16Mo', '59Ni–23Cr–16Mo–1.6Cu', '60Ni–19Cr–19Mo–1.8Ta', '60Ni–22Cr–9Mo–3.5Cb', 
        '60Ni–23Cr–Fe', '60Ni–25Cr–9.5Fe–2.1Al', '61Ni–16Mo–16Cr', '62Ni–22Mo–15Cr', '62Ni–25Mo–8Cr–2Fe', 
        '62Ni–28Mo–5Fe', '65Ni–28Mo–2Fe', '65Ni–29.5Mo–2Fe–2Cr', '67Ni–28Cu–3Al', '67Ni–30Cu', '67Ni–30Cu–S', 
        '70Ni–16Mo–7Cr–5Fe', '72Ni–15Cr–8Fe', '7Ni', '8Ni', '99.2Zr', '99Ni', '99Ni–Low C', '9Cr–1Mo', '9Cr–1Mo–V', 
        '9Ni', 'AlSil2Fe', 'Carbon steel', 'Co–26Cr–9Ni–5Mo–3Fe–2W', 'C–0.3Mo', 'C–Mn–Si–Cb', 'C–Mn–Si–V', 
        'C–Mn–Si–V–Cb', 'C–Mn–Ti', 'C–Si–Ti', 'Ductile cast iron', 'Mn–V', 'Ni–28Mo–3Fe–1.3Cr–0.25Al', 
        'Ni–Cr–Mo–W', 'Ti', 'Ti–0.05Pd', 'Ti–0.10Ru', 'Ti–0.15Pd', 'Ti–0.3Mo–0.8Ni', 'Ti–3Al–2.5V', 'Ti–3Al–2.5V–0.1Ru',
        'Ti–4Al–2.5V–1.5Fe', 'Ti–Pd', 'Ti–Ru']"""

    df = data_frame
    j = df.columns.get_loc('Nominal Composition')

    for i in range(len(df)):

        current = str(df['Nominal Composition'].iloc[i]).strip()

        if '/' not in current:
            continue

        # Searches the master dictionary
        if current in master_translation_dict:
            df.iloc[i, j] = master_translation_dict.get(current)

        # Else tries to perform the adjustment
        else:
            print(f'{str(df["Spec. No."].iloc[i])} {str(df["Type/Grade"].iloc[i])}')
            print(f'{current} composition string not in master dictionary')
            my_new_string = ''
            char_1 = current[0]
            char_2 = current[1]
            char_3 = current[2]
            char_b = current[-2]
            char_l = current[-1]

            if ' /' in current:

                if char_1 == '–':
                    if current.count(' /') == 1:
                        char_2 = current[1]
                        space_position = current.rfind(' /')
                        my_new_string = current[2:space_position] + char_1 + char_2 + current[space_position + 1:]
                    else:
                        my_new_string = current[1:].strip().replace(' ', '-')
                        my_new_string = my_new_string.replace('–/', '/')

                elif char_1.isnumeric():
                    if char_l.isnumeric():
                        position_1 = current.find(' /')
                        position_2 = current.rfind(' /')
                        my_new_string = current[1:position_1] + char_l + current[position_1+1: position_2] +\
                                        char_1 + current[position_2+1:-1].rstrip()

                        if my_new_string[-1].isnumeric():
                            my_new_string = my_new_string[-1] + my_new_string[:-1]

                    elif char_2.isnumeric() or char_2.isalpha():
                        space_position = current.find(' /')
                        my_new_string = current[1:space_position] + char_1 + current[space_position + 1:]

                        if char_l.isnumeric():
                            space_position = current.rfind(' /')
                            my_new_string = current[1:space_position] + char_l + current[space_position + 1:-1]
                            my_new_string.replace(' ', '')

                    elif char_2 == ' ':
                        if char_3.isnumeric():
                            space_position = current.rfind(' /')
                            my_new_string = char_1 + current[3:space_position] + char_3 + \
                                            current[space_position + 1:]

                        elif char_3 == '–':
                            space_position = current.rfind(' /')
                            my_new_string = current[3:space_position] + char_3 + char_1 +  \
                                            current[space_position + 1:]

                        elif char_3 == '/':
                            space_position = current.rfind(' /')
                            my_new_string = char_1 + current[space_position:]

                    else:
                        space_position = current.rfind(' /')
                        my_new_string = current[:space_position] + char_l + current[space_position + 1:-1]

                elif current.count(' ') == 2 and char_l != ' ':
                    last_space_position = current.rfind(' ')
                    first_space_position = current.find(' ')
                    char_after_last_space = current[last_space_position+1]
                    my_new_string = current[:first_space_position] + char_after_last_space + \
                                    current[first_space_position + 1:last_space_position] + \
                                    current[last_space_position + 2:]

                elif current.count(' ') > 2:
                    space_position = current.find(' /')
                    remaining_string = current[space_position + 1:-1]
                    next_space = remaining_string.find(' ')
                    current_char = current[space_position+1+next_space+1]
                    if current_char.isnumeric():
                        my_new_string = current[:space_position] + current_char + \
                                        current[space_position + 1:space_position+1+next_space] + \
                                        current[space_position+1+next_space+2:]

                elif char_l == ' ' and char_b.isnumeric():
                    space_position = current.rfind(' /')
                    my_new_string = current[:space_position] + char_b + \
                                    current[space_position + 1:-2]

                elif ' 1-' in current:
                    space_position = current.find(' /')
                    my_new_string = current[:space_position] + char_b + \
                                    current[space_position + 1:-2]

                elif char_1 == '/':
                    space_position = current.find(' /')
                    my_new_string = '1' + current[:space_position]+'1'+current[space_position:]
                else:
                    my_new_string = current

                my_new_string = my_new_string.replace(' ', '')

            elif '/ ' in current:
                space_position = current.rfind('/ ')
                space_position = space_position + 1
                my_new_string = current[:space_position] + char_l + current[space_position + 1:-1]

            else:
                my_new_string = current.replace(' ', '')

            print(f'Rearranged to {my_new_string}')
            df.iloc[i, j] = my_new_string

    return df


def read_single_page(pdf_path, pdf_page, top, bottom, left, right, columns_positions, columns_names):
    """
    Main method to read the PDF page, one at a time.
    input:
        pdf_path            - STR: PDF file path
        pdf_page            - INT: PDF page number
        top                 - INT: table start, distance from the top
        bottom              - INT: table finish: distance from the top
        left                - INT: table start: distance from the left
        right               - INT: table finish: distance from the left
        columns_positions   - LIST: list with the columns end positions starting from the left
        columns_names       - LIST: list with the columns names

    returns: PANDAS dataframe
    """
    print(f'Extracting page {pdf_page}')
    dfs = tabula.read_pdf(pdf_path, pages=pdf_page, guess=False, encoding='utf-8',
                          multiple_tables=False, area=[top, left, bottom, right], columns=columns_positions,
                          pandas_options={'header': None, "dtype": str, "keep_default_na": True,
                                          "skip_blank_lines": False})
    df = dfs[0]
    df = clear_table(df)
    df = df.dropna()
    df = df.reset_index(drop=True)
    df.columns = columns_names

    return df


def read_table_group(pdf_path, page_start, page_finish, boundaries_dict, columns_names_dict):
    """
    Intermediary function that will concatenate the tables as per the required grouping
    input:
        pdf_path            - STR: PDF file path
        page_start          - INT: start page from the PDF file
        page_finish         - INT: finish page from the PDF file
        boundaries_dict     - DICT: dictionary with the table boundaries
        columns_names_dict  - DICT: dictionary with the columns names

    returns: PANDAS dataframe
    """

    df_temp = pd.DataFrame()
    count = 1

    for i in range(page_start, page_finish+1):
        boundaries = boundaries_dict[str(count)]
        columns_names = columns_names_dict[str(count)]
        top = boundaries['Top Border']
        left = boundaries['Left Border']
        right = boundaries['Right Border']
        bottom = boundaries['Bottom Border']
        internal_borders = [v for k, v in boundaries.items() if 'Col.' in k and int(v) != 0]
        new_data = read_single_page(pdf_path, i, top, bottom, left, right, internal_borders, columns_names)
        internal_borders.insert(0, left)

        # print(f'\tReading page {i}')
        # print(f'\tApplicable boundaries:{boundaries}')
        # print(f'\tApplicable columns names: {columns_names}')
        # print(f'\tMain borders: {top}, {left}, {bottom}, {right}')
        # print(f'\tAll columns borders: {internal_borders}')
        # print(f'\tSize Comparison: {len(internal_borders)} == {len(columns_names)}')

        if df_temp.empty:
            df_temp = new_data
        else:
            df_temp = pd.merge(df_temp, new_data, how='inner')
        count += 1

    return df_temp


def read_pdf_table(pdf_path, page_start, page_end, pages_per_table, page_skip, boundaries_dict, columns_names, parent):
    """
    Function that will organize and extract the tables from the PDF file
    input:
        pdf_path        - STR: PDF file path
        page_start      - INT: PDF starting page
        page_end        - INT: PDF end page
        pages_per_table - INT: number of pages that comprise the table
        page_skip       - INT: pages to skip in between the tables
        boundaries_dict - DICT: dictionary with the table boundaries
        columns_names   - DICT: dictionary with the columns names

    returns: PANDAS dataframe
    """

    # print(f'Read PDF Table method called')
    # print(f'Input Data:')
    # print(f'\tPDF file path: {pdf_path}')
    # print(f'\tPDF page start: {page_start}')
    # print(f'\tPDF page end: {page_end}')
    # print(f'\tPDF pages per table: {pages_per_table}')
    # print(f'\tPDF page to skip: {page_skip}')
    # print(f'\tBoundaries values: {boundaries_dict}')
    # print(f'\tColumns names: {columns_names}\n')

    df = pd.DataFrame()
    page_grouping = pages_per_table + page_skip

    count = 0
    total = page_end - page_start + 1
    progress_bar = cw.ProgressBar(parent, message='Extracting selected pages ...', final_value=total)
    progress_bar.grab_set()
    for current_page in range(page_start, page_end, page_grouping):
        count += 1
        progress_bar.update_bar(count)
        group_starting_page = current_page
        group_finish_page = current_page + pages_per_table - 1
        df_temp = read_table_group(pdf_path, group_starting_page, group_finish_page, boundaries_dict, columns_names)
        if df.empty:
            df = df_temp
        else:
            df = pd.concat([df, df_temp])
    progress_bar.destroy()
    df = df.reset_index(drop=True)
    df = adjust_chemical_composition(df)
    # print('Extraction finished')
    return df

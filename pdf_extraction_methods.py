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


def adjust_chemical_composition(data_frame, chemical_composition_dict):
    """ Adjust the chemical composition read from file """

    master_translation_dict = {
        '1C– /4Mo': 'C–1/4Mo',
        'C– /4Mo': 'C–1/4Mo',
        'C –1/4Mo': 'C–1/4Mo',

        '1C– /2Mo': 'C–1/2Mo',
        'C– /2Mo': 'C–1/2Mo',
        'C –1/2Mo': 'C–1/2Mo',

        '1 1/2Cr– /5Mo': '1/2Cr–1/5Mo',
        '/2Cr– /5Mo': '1/2Cr–1/5Mo',
        '1 /2Cr –1/5Mo': '1/2Cr–1/5Mo',
        '/2Cr–1/5Mo': '1/2Cr–1/5Mo',

        '1 1/2Cr– /5Mo–V': '1/2Cr–1/5Mo–V',
        '/2Cr– /5Mo–V': '1/2Cr–1/5Mo–V',
        '1 /2Cr –1/5Mo–V': '1/2Cr–1/5Mo–V',
        '/2Cr–1/5Mo–V': '1/2Cr–1/5Mo–V',

        '1 1/2Cr– /4Mo–Si': '1/2Cr–1/4Mo–Si',
        '/2Cr– /4Mo–Si': '1/2Cr–1/4Mo–Si',
        '1 /2Cr –1/4Mo–Si': '1/2Cr–1/4Mo–Si',

        '1 /2Cr– /2Mo1': '1/2Cr–1/2Mo',
        '1 /2Cr –1/2Mo': '1/2Cr–1/2Mo',
        '1 1/2Cr– /2Mo': '1/2Cr–1/2Mo',
        '/2Cr– /2Mo': '1/2Cr–1/2Mo',
        '/2Cr–1/2Mo': '1/2Cr–1/2Mo',

        '3 1/4Cr– /2Ni–Cu': '3/4Cr–1/2Ni–Cu',
        '/4Cr– /2Ni–Cu': '3/4Cr–1/2Ni–Cu',
        '3 /4Cr –1/2Ni–Cu': '3/4Cr–1/2Ni–Cu',

        '3 3/4Cr– /4Ni–Cu–Al': '3/4Cr–3/4Ni–Cu–Al',
        '/4Cr– /4Ni–Cu–Al':  '3/4Cr–3/4Ni–Cu–Al',

        '11Cr– /5Mo': '1Cr–1/5Mo',
        '1Cr– /5Mo':  '1Cr–1/5Mo',
        '1Cr –1/5Mo': '1Cr–1/5Mo',
        '11Cr– /2Mo': '1Cr–1/2Mo',
        '1Cr– /2Mo': '1Cr–1/2Mo',
        '1Cr–1/2Mo': '1Cr–1/2Mo',
        '1Cr –1/2Mo': '1Cr–1/2Mo',
        '11Cr– /2Mo–V': '1Cr–1/2Mo–V',
        '1Cr– /2Mo–V': '1Cr–1/2Mo–V',
        '11Cr– /4Si–V': '1Cr–1/4Si–V',
        '1Cr–1Mn– /4Mo': '1Cr–1Mn–1/4Mo',

        '11 /4Cr– /2Mo1': '1 1/4Cr–1/2Mo',
        '1 /4Cr– /2Mo': '1 1/4Cr–1/2Mo',
        '1 /4Cr–1/2Mo': '1 1/4Cr–1/2Mo',
        '1 1 /4Cr –1/2Mo': '1 1/4Cr–1/2Mo',
        '11 /4Cr– /2Mo–Si1': '1 1/4Cr–1/2Mo–Si',
        '1 1 /4Cr– /2Mo–Si1': '1 1/4Cr–1/2Mo–Si',
        '1 /4Cr–1/2Mo–Si':  '1 1/4Cr–1/2Mo–Si',
        '1 1 /4Cr –1/2Mo–Si': '1 1/4Cr–1/2Mo–Si',
        '1 /4Cr– /2Mo–Si': '1 1/4Cr–1/2Mo–Si',

        '1 /4Cr– /2Mo–Cu': '1 3/4Cr–1/2Mo–Cu',
        '11 /4Cr– /2Mo–Cu3': '1 3/4Cr–1/2Mo–Cu',
        '3 1 /4Cr –1/2Mo–Cu': '1 3/4Cr–1/2Mo–Cu',

        '11 /4Cr– /2Mo–Ti3': '1 3/4Cr–1/2Mo–Ti',
        '1 /4Cr– /2Mo–Ti': '1 3/4Cr–1/2Mo–Ti',
        '1 /4Cr–1/2Mo–Ti': '1 3/4Cr–1/2Mo–Ti',

        '12 /4Cr–1Mo': '2 1/4Cr–1Mo',
        '2 /4Cr–1Mo': '2 1/4Cr–1Mo',
        '1 2 /4Cr 1Mo–': '2 1/4Cr–1Mo',
        '12 /4Cr–1Mo–V': '2 1/4Cr–1Mo–V',
        '2 /4Cr–1Mo–V': '2 1/4Cr–1Mo–V',

        '13Cr–1Mo– /4V–Ti–B': '3Cr–1Mo–1/4V–Ti–B',
        '3Cr–1Mo– /4V–Ti–B': '3Cr–1Mo–1/4V–Ti–B',
        '3Cr–1Mo–1/4V–Ti–B': '3Cr–1Mo–1/4V–Ti–B',
        '3Cr– 11Mo– /4V–Ti–B': '3Cr–1Mo–1/4V–Ti–B',
        '3Cr 1Mo– /4V–Ti–B– 1': '3Cr–1Mo–1/4V–Ti–B',

        '13Cr–1Mo– /4V–Cb–Ca': '3Cr–1Mo–1/4V–Cb–Ca',
        '3Cr–1Mo– /4V–Cb–Ca': '3Cr–1Mo–1/4V–Cb–Ca',
        '3Cr– 11Mo– /4V–Cb–Ca': '3Cr–1Mo–1/4V–Cb–Ca',
        '3Cr–1Mo–1/4V–Cb–Ca': '3Cr–1Mo–1/4V–Cb–Ca',

        '15Cr– /2Mo': '5Cr–1/2Mo',
        '5Cr– /2Mo': '5Cr–1/2Mo',
        '5Cr –1/2Mo': '5Cr–1/2Mo',
        '5Cr–1/2Mo': '5Cr–1/2Mo',
        '15Cr– /2Mo–Si': '5Cr–1/2Mo–Si',
        '5Cr– /2Mo–Si': '5Cr–1/2Mo–Si',
        '15Cr– /2Mo–Ti': '5Cr–1/2Mo–Ti',
        '5Cr– /2Mo–Ti': '5Cr–1/2Mo–Ti',

        '1Mn– /4Mo': 'Mn–1/4Mo',
        'Mn– /4Mo': 'Mn–1/4Mo',
        'Mn –1/4Mo': 'Mn–1/4Mo',
        '1Mn– /4Mo–V': 'Mn–1/4Mo–V',
        'Mn– /4Mo–V': 'Mn–1/4Mo–V',
        '1Mn– /2Mo': 'Mn–1/2Mo',
        'Mn– /2Mo': 'Mn–1/2Mo',
        'Mn –1/2Mo': 'Mn–1/2Mo',

        '1Mn– /2Mo– /4Ni1': 'Mn–1/2Mo–1/4Ni',
        'Mn– /2Mo– /4Ni': 'Mn–1/2Mo–1/4Ni',
        'Mn–1 1/2Mo– /4Ni': 'Mn–1/2Mo–1/4Ni',
        'Mn –1 /2Mo– /4Ni1': 'Mn–1/2Mo–1/4Ni',
        'Mn –1/2Mo–1/4Ni': 'Mn–1/2Mo–1/4Ni',

        '1Mn– /2Mo– /2Ni1': 'Mn–1/2Mo–1/2Ni',
        'Mn– /2Mo– /2Ni': 'Mn–1/2Mo–1/2Ni',
        'Mn –1 /2Mo –1/2Ni': 'Mn–1/2Mo–1/2Ni',
        'Mn –1 /2Mo– /2Ni1': 'Mn–1/2Mo–1/2Ni',
        'Mn–1 1/2Mo– /2Ni':  'Mn–1/2Mo–1/2Ni',

        '3Mn– /2Mo– /4Ni1': 'Mn–1/2Mo–3/4Ni',
        'Mn–1/2Mo–3/4Ni': 'Mn–1/2Mo–3/4Ni',
        'Mn –1 /2Mo –3/4Ni': 'Mn–1/2Mo–3/4Ni',
        'Mn– /2Mo–3/4Ni': 'Mn–1/2Mo–3/4Ni',
        'Mn –1 /2Mo– /4Ni3': 'Mn–1/2Mo–3/4Ni',

        '1Mn– /2Ni–V': 'Mn–1/2Ni–V',
        'Mn– /2Ni–V': 'Mn–1/2Ni–V',
        'Mn –1/2Ni–V': 'Mn–1/2Ni–V',

        '11 /2Si– /2Mo1': '1 1/2Si–1/2Mo',
        '1 /2Si– /2Mo': '1 1/2Si–1/2Mo',

        '1 1/2Ni– /2Cr– /4Mo–V1': '1/2Ni–1/2Cr–1/4Mo–V',
        '/2Ni– /2Cr– /4Mo–V':  '1/2Ni–1/2Cr–1/4Mo–V',
        '1 /2Ni –1 /2Cr –1/4Mo–V': '1/2Ni–1/2Cr–1/4Mo–V',
        '1 /2Ni –1 /2Cr– /4Mo–V1': '1/2Ni–1/2Cr–1/4Mo–V',
        '1 1/2Ni– /2Mo–V': '1/2Ni–1/2Mo–V',
        '/2Ni– /2Mo–V': '1/2Ni–1/2Mo–V',
        '1 /2Ni –1/2Mo–V': '1/2Ni–1/2Mo–V',

        '3 1/4Ni– /2Cr– /2Mo–V1': '3/4Ni–1/2Cr–1/2Mo–V',
        '/4Ni– /2Cr– /2Mo–V': '3/4Ni–1/2Cr–1/2Mo–V',
        '3 /4Ni –1 /2Cr– /2Mo–V1': '3/4Ni–1/2Cr–1/2Mo–V',
        '/4Ni–1 1/2Cr– /2Mo–V': '3/4Ni–1/2Cr–1/2Mo–V',

        '3 1/4Ni– /2Cu–Mo': '3/4Ni–1/2Cu–Mo',
        '3 /4Ni –1/2Cu–Mo': '3/4Ni–1/2Cu–Mo',
        '/4Ni– /2Cu–Mo': '3/4Ni–1/2Cu–Mo',

        '3 1/4Ni– /2Mo– /3Cr–V1': '3/4Ni–1/2Mo–1/3Cr–V',
        '/4Ni– /2Mo– /3Cr–V': '3/4Ni–1/2Mo–1/3Cr–V',
        '/4Ni–1/2Mo–1/3Cr–V': '3/4Ni–1/2Mo–1/3Cr–V',
        '3 /4Ni –1 /2Mo– /3Cr–V1': '3/4Ni–1/2Mo–1/3Cr–V',

        '3 1/4Ni– /2Mo–Cr–V': '3/4Ni–1/2Mo–Cr–V',
        '/4Ni– /2Mo–Cr–V': '3/4Ni–1/2Mo–Cr–V',
        '3 /4Ni –1/2Mo–Cr–V': '3/4Ni–1/2Mo–Cr–V',

        '3 3/4Ni–1Mo– /4Cr': '3/4Ni–1Mo–3/4Cr',
        '/4Ni–1Mo– /4Cr': '3/4Ni–1Mo–3/4Cr',
        '3 /4Ni 1Mo – –3/4Cr': '3/4Ni–1Mo–3/4Cr',
        '/4Ni–1Cu– /4Cr': '3/4Ni–1Cu–3/4Cr',

        '11Ni– /2Cr– /2Mo1': '1Ni–1/2Cr–1/2Mo',
        '1Ni –1 /2Cr– /2Mo1': '1Ni–1/2Cr–1/2Mo',
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
        '2Ni 1 /2Cr– /4Mo–V– 1 1': '2Ni–1 1/2Cr–1/4Mo–V',
        '2Ni 1 /2Cr – 1 –1/4Mo–V': '2Ni–1 1/2Cr–1/4Mo–V',

        '12 /2Ni': '2 1/2Ni',
        '2 /2Ni': '2 1/2Ni',
        '12 /4Ni–1 /2Cr– /2Mo3 1': '2 3/4Ni–1 1/2Cr–1/2Mo',
        '2 /4Ni–1 /2Cr– /2Mo': '2 3/4Ni–1 1/2Cr–1/2Mo',
        '2 /4Ni–1 /2Cr–1/2Mo': '2 3/4Ni–1 1/2Cr–1/2Mo',
        '2 /4Ni 1 /2Cr–3 – 11/2Mo': '2 3/4Ni–1 1/2Cr–1/2Mo',

        '12 /4Ni–1 /2Cr– /2Mo–V3 1': '2 3/4Ni–1 1/2Cr–1/2Mo–V',
        '2 /4Ni–1 /2Cr– /2Mo–V': '2 3/4Ni–1 1/2Cr–1/2Mo–V',
        '2 /4Ni–1 /2Cr–1/2Mo–V': '2 3/4Ni–1 1/2Cr–1/2Mo–V',
        '2 /4Ni–11 /2Cr– /2Mo–V1': '2 3/4Ni–1 1/2Cr–1/2Mo–V',
        '2 /4Ni 1 /2Cr– /2Mo–V3 – 1 1': '2 3/4Ni–1 1/2Cr–1/2Mo–V',

        '13Ni–1 /4Cr– /2Mo3': '3Ni–1 3/4Cr–1/2Mo',
        '3Ni–1 /4Cr– /2Mo': '3Ni–1 3/4Cr–1/2Mo',
        '3Ni 1 /4Cr– /2Mo– 3 1': '3Ni–1 3/4Cr–1/2Mo',
        '3Ni–1 /4Cr–1/2Mo': '3Ni–1 3/4Cr–1/2Mo',
        '13 /2Ni': '3 1/2Ni',
        '3 /2Ni': '3 1/2Ni',
        '13 /2Ni–1 /4Cr– /2Mo–V1 3': '3 1/2Ni–1 3/4Cr–1/2Mo–V',
        '3 /2Ni–1 /4Cr– /2Mo–V': '3 1/2Ni–1 3/4Cr–1/2Mo–V',
        '3 /2Ni 1 /4Cr– /2Mo–V1 – 3 1': '3 1/2Ni–1 3/4Cr–1/2Mo–V',
        '14Ni–1 /2Cr– /2Mo–V1': '4Ni–1 1/2Cr–1/2Mo–V',
        '4Ni–1 /2Cr– /2Mo–V': '4Ni–1 1/2Cr–1/2Mo–V',
        '4Ni 1 /2Cr– /2Mo–V– 1 1': '4Ni–1 1/2Cr–1/2Mo–V',
        '4Ni– 11 /2Cr– /2Mo–V1': '4Ni–1 1/2Cr–1/2Mo–V',
        '15Ni– /4Mo': '5Ni–1/4Mo',
        '5Ni– /4Mo': '5Ni–1/4Mo',
        '5Ni–1/4Mo': '5Ni–1/4Mo',

        '12 /2Cr–2Ni': '12 1/2Cr–2Ni',
        '135Ni–19Cr–1 /4Si': '35Ni–19Cr–1 1/4Si',
        '35Ni–19Cr–1 /4Si': '35Ni–19Cr–1 1/4Si',
        '119Cr–9Ni– /2Mo': '19Cr–9Ni–1/2Mo',
        '19Cr–9Ni– /2Mo': '19Cr–9Ni–1/2Mo',
        '19Cr 9Ni – –1/2Mo': '19Cr–9Ni–1/2Mo',
        '19Cr–9Ni–1/2Mo': '19Cr–9Ni–1/2Mo',
    }

    df = data_frame
    j = df.columns.get_loc('Nominal Composition')

    for i in range(len(df)):

        # Assembles material identifier
        if True:
            try:
                _spec = str(df["Spec. No."].iloc[i])
            except KeyError:
                _spec = ''

            try:
                _type = str(df["Type/Grade"].iloc[i])
            except KeyError:
                _type = ''

            try:
                _alloy = str(df["Alloy Desig./UNS No."].iloc[i])
            except KeyError:
                _alloy = ''

            try:
                _condition = str(df["Class/Condition/Temper"].iloc[i])
            except KeyError:
                _condition = ''
        identifier = f'{_spec} {_type} {_alloy} {_condition}'
        current_chemical_string = str(df['Nominal Composition'].iloc[i]).strip()

        if identifier in chemical_composition_dict:
            chemical_composition = chemical_composition_dict[identifier]

        elif '/' not in current_chemical_string:
            chemical_composition_dict[identifier] = current_chemical_string
            chemical_composition = current_chemical_string

        else:
            if current_chemical_string in master_translation_dict:
                chemical_composition = master_translation_dict.get(current_chemical_string)
                chemical_composition_dict[identifier] = chemical_composition

            else:
                print(f'The following chemical composition does not exist in the current database')
                print(f'{_spec} {_type} {_alloy} {_condition}')
                print(f'What is the desired chemical composition string?', end=' ')
                chemical_composition = input()
                chemical_composition_dict[identifier] = chemical_composition

        df.iloc[i, j] = chemical_composition

    return df, chemical_composition_dict


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
        count += page_grouping
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

    # Adjust the chemical composition for the material specifications
    chemical_composition_data = parent.chemical_composition_data
    df, new_chemical_composition_data = adjust_chemical_composition(df, chemical_composition_data)
    chemical_composition_data.update(new_chemical_composition_data)
    # print('Extraction finished')

    return df

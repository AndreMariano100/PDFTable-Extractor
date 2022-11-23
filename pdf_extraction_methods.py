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

        '11 /4Cr– /2Mo1': '11/4Cr–1/2Mo',
        '1 /4Cr– /2Mo': '11/4Cr–1/2Mo',
        '11 /4Cr– /2Mo–Si1': '11/4Cr–1/2Mo–Si',
        '1 1 /4Cr– /2Mo–Si1': '11/4Cr–1/2Mo–Si',
        '1 /4Cr– /2Mo–Si': '11/4Cr–1/2Mo–Si',

        '1 /4Cr– /2Mo–Cu': '13/4Cr–1/2Mo–Cu',
        '11 /4Cr– /2Mo–Cu3': '13/4Cr–1/2Mo–Cu',
        '11 /4Cr– /2Mo–Ti3': '13/4Cr–1/2Mo–Ti',
        '1 /4Cr– /2Mo–Ti': '13/4Cr–1/2Mo–Ti',

        '12 /4Cr–1Mo': '21/4Cr–1Mo',
        '2 /4Cr–1Mo': '21/4Cr–1Mo',
        '12 /4Cr–1Mo–V': '21/4Cr–1Mo–V',
        '2 /4Cr–1Mo–V': '21/4Cr–1Mo–V',

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

        '11 /2Si– /2Mo1': '11/2Si–1/2Mo',
        '1 /2Si– /2Mo': '11/2Si–1/2Mo',

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
        '11 /4Ni–1Cr– /2Mo1': '11/4Ni–1Cr–1/2Mo',
        '1 /4Ni–1Cr– /2Mo': '11/4Ni–1Cr–1/2Mo',
        '11 /2Ni': '11/2Ni',
        '1 /2Ni': '11/2Ni',
        '11 /4Ni– /4Cr– /4Mo3 3': '13/4Ni–3/4Cr–1/4Mo',
        '1 /4Ni– /4Cr– /4Mo': '13/4Ni–3/4Cr–1/4Mo',
        '1 /4Ni– /4Cr–Mo': '13/4Ni–3/4Cr–1Mo',

        '12Ni– /4Cr– /4Mo3': '2Ni–3/4Cr–1/4Mo',
        '2Ni– /4Cr– /4Mo': '2Ni–3/4Cr–1/4Mo',
        '12Ni– /4Cr– /3Mo3': '2Ni–3/4Cr–1/3Mo',
        '2Ni– /4Cr– /3Mo': '2Ni–3/4Cr–1/3Mo',
        '12Ni–1 /2Cr– /4Mo–V1': '2Ni–11/2Cr–1/4Mo–V',
        '2Ni–1 /2Cr– /4Mo–V': '2Ni–11/2Cr–1/4Mo–V',

        '12 /2Ni': '21/2Ni',
        '2 /2Ni': '21/2Ni',
        '12 /4Ni–1 /2Cr– /2Mo3 1': '23/4Ni–11/2Cr–1/2Mo',
        '2 /4Ni–1 /2Cr– /2Mo': '23/4Ni–11/2Cr–1/2Mo',
        '12 /4Ni–1 /2Cr– /2Mo–V3 1': '23/4Ni–11/2Cr–1/2Mo–V',
        '2 /4Ni–1 /2Cr– /2Mo–V': '23/4Ni–11/2Cr–1/2Mo–V',

        '13Ni–1 /4Cr– /2Mo3': '3Ni–13/4Cr–1/2Mo',
        '3Ni–1 /4Cr– /2Mo': '3Ni–13/4Cr–1/2Mo',
        '13 /2Ni': '31/2Ni',
        '3 /2Ni': '31/2Ni',
        '13 /2Ni–1 /4Cr– /2Mo–V1 3': '31/2Ni–13/4Cr–1/2Mo–V',
        '3 /2Ni–1 /4Cr– /2Mo–V': '31/2Ni–13/4Cr–1/2Mo–V',
        '14Ni–1 /2Cr– /2Mo–V1': '4Ni–11/2Cr–1/2Mo–V',
        '4Ni–1 /2Cr– /2Mo–V': '4Ni–11/2Cr–1/2Mo–V',
        '15Ni– /4Mo': '5Ni–1/4Mo',
        '5Ni– /4Mo': '5Ni–1/4Mo',

        '135Ni–19Cr–1 /4Si': '35Ni–19Cr–11/4Si',
        '35Ni–19Cr–1 /4Si': '35Ni–19Cr–11/4Si',
        '119Cr–9Ni– /2Mo': '19Cr–9Ni–1/2Mo',
        '19Cr–9Ni– /2Mo': '19Cr–9Ni–1/2Mo',
    }

    def clean_labels(df):

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

    if data_frame is None:
        import os
        from tkinter.filedialog import askopenfilename

        try:
            desktop = os.path.normpath(os.path.expanduser("~/Desktop"))
            file_name = askopenfilename(initialdir=desktop, title="Select File",
                                        filetypes=(("CSV files", "*.csv"),
                                                   ("All files", "*.*")))
        except IOError or FileNotFoundError:
            return
        else:
            if not file_name:
                return

        local_data_frame = pd.read_csv(file_name, sep=';')
    else:
        local_data_frame = data_frame

    new_df = clean_labels(local_data_frame)

    return new_df


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
        internal_borders = [v for k, v in boundaries.items() if 'End' in k and int(v) != 0]
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


if __name__ == '__main__':
    adjust_chemical_composition()

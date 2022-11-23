import pandas as pd
import tabula


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

    def clean_labels(df):

        j = df.columns.get_loc('Nominal Composition')
        cases_count = {}

        for i in range(len(df)):

            current = str(df['Nominal Composition'].iloc[i])

            if '/' not in current:
                continue

            my_new_string = ''
            char_1 = current[0]
            char_2 = current[1]
            char_3 = current[2]
            char_4 = current[4]
            char_b = current[-2]
            char_l = current[-1]

            case = ''

            if ' /' in current:

                if char_1 == '–':
                    if current.count(' /') == 1:
                        char_2 = current[1]
                        space_position = current.rfind(' /')
                        my_new_string = current[2:space_position] + char_1 + char_2 + current[space_position + 1:]
                        case = 'case 1'
                    else:
                        my_new_string = current[1:].strip().replace(' ', '-')
                        my_new_string = my_new_string.replace('–/', '/')
                        case = 'case 1 modified'

                    # "–11 /4Cr 1 /2Mo–Si" -> "1/4Cr1–1/2Mo–Si"
                    # "–11Cr /4Si–V" -> "1Cr–1/4Si–V"
                    # "–1C /4Mo" -> "C–1/4Mo"

                elif char_1.isnumeric():

                    if char_l.isnumeric():
                        position_1 = current.find(' /')
                        position_2 = current.rfind(' /')

                        my_new_string = current[1:position_1] + char_l + current[position_1+1: position_2] +\
                                        char_1 + current[position_2+1:-1].rstrip()
                        case = 'case 2'

                        if my_new_string[-1].isnumeric():
                            my_new_string = my_new_string[-1] + my_new_string[:-1]
                            case = 'case 2 modified'

                    elif char_2.isnumeric() or char_2.isalpha():
                        space_position = current.find(' /')
                        my_new_string = current[1:space_position] + char_1 + current[space_position + 1:]
                        case = 'case 3'
                        if char_l.isnumeric():
                            space_position = current.rfind(' /')
                            my_new_string = current[1:space_position] + char_l + current[space_position + 1:-1]
                            my_new_string.replace(' ', '')
                            case = 'case 4'

                    elif char_2 == ' ':
                        if char_3.isnumeric():
                            space_position = current.rfind(' /')
                            my_new_string = char_1 + current[3:space_position] + char_3 + current[space_position + 1:]
                            case = 'case 5'

                        elif char_3 == '–':
                            space_position = current.rfind(' /')
                            my_new_string = current[3:space_position] + char_3 + char_1 + \
                                            current[space_position + 1:]
                            case = 'case 6'

                        elif char_3 == '/':

                            space_position = current.rfind(' /')
                            my_new_string = char_1 + current[space_position:]
                            case = 'case 7'

                    else:
                        space_position = current.rfind(' /')
                        my_new_string = current[:space_position] + char_l + current[space_position + 1:-1]
                        case = 'case 8'

                elif current.count(' ') == 2 and char_l != ' ':
                    last_space_position = current.rfind(' ')
                    first_space_position = current.find(' ')
                    char_after_last_space = current[last_space_position+1]
                    my_new_string = current[:first_space_position] + char_after_last_space + \
                                    current[first_space_position + 1:last_space_position] + \
                                    current[last_space_position + 2:]
                    case = 'case 9'

                elif current.count(' ') > 2:
                    space_position = current.find(' /')
                    remaining_string = current[space_position + 1:-1]
                    next_space = remaining_string.find(' ')
                    current_char = current[space_position+1+next_space+1]
                    if current_char.isnumeric():
                        my_new_string = current[:space_position] + current_char + \
                                        current[space_position + 1:space_position+1+next_space] + \
                                        current[space_position+1+next_space+2:]
                        case = 'case 10'

                elif char_l == ' ' and char_b.isnumeric():
                    space_position = current.rfind(' /')
                    my_new_string = current[:space_position] + char_b + \
                                    current[space_position + 1:-2]
                    case = 'case 11'

                elif ' 1-' in current:
                    space_position = current.find(' /')
                    my_new_string = current[:space_position] + char_b + \
                                    current[space_position + 1:-2]
                    case = 'case 12'

                else:
                    case = 'case 13'
                    my_new_string = current

                my_new_string = my_new_string.replace(' ', '')

                df.iloc[i, j] = my_new_string

            elif '/ ' in current:
                space_position = current.rfind('/ ')
                space_position = space_position + 1
                my_new_string = current[:space_position] + char_l + current[space_position + 1:-1]

                df.iloc[i, j] = my_new_string

            else:
                case = 'case 14'
                my_new_string = current.replace(' ', '')

            if case not in cases_count:
                cases_count[case] = 1
            else:
                cases_count[case] += 1

            if case:
                print(f'{case}: "{current}" -> "{my_new_string}"')
            else:
                print(f'"{current}", {case}')
                input()

        print(cases_count)

        return df

    if not data_frame:
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

    old_values = local_data_frame['Nominal Composition'].tolist()
    new_values = new_df['Nominal Composition'].tolist()

    for a, b in zip(old_values, new_values):
        if a != b:
            print(f'{a} -> {b}')


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
                          area=[top, left, bottom, right], columns=columns_positions)
    if not dfs:
        print('Empty table error')
        return

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
        
        # print(f'\tReading page {i}')
        # print(f'\tApplicable boundaries:{boundaries}')
        # print(f'\tApplicable columns names: {columns_names}')
        # print(f'\tMain borders: {top}, {left}, {bottom}, {right}')
        # internal_borders.insert(0, left)
        # print(f'\tAll columns borders: {internal_borders}')
        
        if df_temp.empty:
            df_temp = new_data
        else:
            df_temp = pd.concat([df_temp, new_data], axis=1, join='inner')
        count += 1

    return df_temp


def read_pdf_table(pdf_path, page_start, page_end, pages_per_table, page_skip, boundaries_dict, columns_names):
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

    for current_page in range(page_start, page_end, page_grouping):
        group_starting_page = current_page
        group_finish_page = current_page + pages_per_table - 1
        df_temp = read_table_group(pdf_path, group_starting_page, group_finish_page, boundaries_dict, columns_names)
        if df.empty:
            df = df_temp
        else:
            df = pd.concat([df, df_temp])
    df = df.reset_index(drop=True)
    # print('Extraction finished')
    return df


if __name__ == '__main__':
    adjust_chemical_composition()

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

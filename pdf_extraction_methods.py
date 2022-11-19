import pandas as pd
import tabula


def clear_table(df):
    """ Method to clear the table from extraction artifacts: ('-', ',', '`', ' ') """

    for i in range(len(df)):
        for j in range(len(df.columns)):
            my_string = str(df.iloc[i, j])
            if '-' in my_string or '`' in my_string:
                my_string = my_string.replace('-', '')
                my_string = my_string.replace(' ', '')
                my_string = my_string.replace(',', '')
                my_string = my_string.replace('`', '')
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

    dfs = tabula.read_pdf(pdf_path, pages=pdf_page, guess=False,
                          area=[top, left, bottom, right], columns=columns_positions)
    if not dfs:
        print('Empty table error')
        return

    print(dfs)
    df = dfs[0]
    print(df)
    df = clear_table(df)
    df = df.dropna()
    df = df.reset_index(drop=True)
    df.columns = columns_names

    return df


def read_group_table(pdf_path, page_start, page_finish, boundaries_dict, columns_names_dict):
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

    df_temp = []
    df = pd.DataFrame()
    count = 1

    for i in range(page_start, page_finish+1):
        boundaries = boundaries_dict[str(count)]
        columns_names = columns_names_dict[str(count)]
        top = boundaries['Top Border']
        left = boundaries['Left Border']
        right = boundaries['Right Border']
        bottom = boundaries['Bottom Border']
        internal_borders = [v for k, v in boundaries.items() if 'End' in k and int(v) != 0]
        internal_borders.insert(0, left)
        df_temp.append(read_single_page(pdf_path, i, top, bottom, left, right, internal_borders, columns_names))
        count += 1

    df = pd.concat(df_temp, axis=1)
    return df


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

    df = pd.DataFrame()
    page_grouping = pages_per_table + page_skip
    total = page_end - page_start

    for current_page in range(page_start, page_end, page_grouping):
        group_starting_page = current_page
        group_finish_page = current_page + pages_per_table
        df_temp = read_group_table(pdf_path, group_starting_page, group_finish_page, boundaries_dict, columns_names)
        df = df.append(df_temp)

        completion = 100*(current_page / total)
        print(f'{completion:.1f} %')
    df = df.reset_index(drop=True)
    return df

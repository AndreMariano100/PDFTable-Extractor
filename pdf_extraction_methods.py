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
        top                 - STR: '%10' table start, distance from the top (percent of the page height)
        bottom              - STR: '%90' table finish: distance from the top (percent of the page height)
        left                - STR: '%10' table start: distance from the left (percent of the page width)
        right               - STR: '%90' table finish: distance from the left (percent of the page width)
        columns_positions   - LIST: list with the columns positions starting from the left
        columns_names       - LIST: list with the columns names

    returns: PANDAS dataframe
    """

    dfs = tabula.read_pdf(pdf_path, pages=pdf_page, guess=False, relative_area=True,
                          area=[top, left, bottom, right], columns=columns_positions)
    print(dfs)
    df = dfs[0]
    print(df)
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

    for current_page in range(page_start, page_end, page_grouping):
        df_temp = read_table_group(pdf_path, current_page, pages_per_table, page_skip, boundaries_dict, columns_names)
        df = df.append(df_temp)
        completion = 100*(current_page+(page_grouping-1)-page_start)/(page_end-page_start)
        print(f'{completion:.2f} %')
    df = df.reset_index(drop=True)
    return df


def read_table_group(pdf_path, current_page, pages_per_table, page_skip, boundaries_dict, columns_names):
    """
    Intermediary function that will concatenate the tables as per the required grouping
    input:
        pdf_path        - STR: PDF file path
        page_skip       - INT: pages to skip in between the tables
        boundaries_dict - DICT: dictionary with the table boundaries
        columns_names   - DICT: dictionary with the columns names

    returns: PANDAS dataframe
    """

    df_temp = []
    df = pd.DataFrame()

    for i in range(pages_per_table):
        current_page_pattern_number = i+1
        if current_page_pattern_number not in page_skip:
            df_temp.append(Read(pdf_path,page_start+i,top[i],left[i],width[i],height[i],columns_spaces[i],columns_names[i],clear_table[i]))
            # df_temp.append(read_pdf_page(pdf_path, pdf_page, top, bottom, left, right, columns_positions, columns_names)
            if i>0:
                df_temp[i].drop(df_temp[i].columns[0], axis=1, inplace=True)

    df = pd.concat([df_temp[i] for i in range(pages_per_table)], axis=1)
    return df

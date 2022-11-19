import pandas as pd
import Assembly_Table


# Função para corrigir a coluna composição nominal
# def corrigir_composicao_nominal(df):
#     if "Nominal Composition" in df.columns:
#         for i in range(len(df['Nominal Composition'])):
#             j = df.columns.get_loc('Nominal Composition')
#             if ' /' in df['Nominal Composition'].iloc[i]:
#                 first_position_in_string = df['Nominal Composition'].iloc[i][0]
#                 if first_position_in_string == '–':
#                     second_position_in_string = df['Nominal Composition'].iloc[i][1]
#                     space_position = df['Nominal Composition'].iloc[i].find(' /')
#                     my_new_string = df['Nominal Composition'].iloc[i][2:space_position] + \
#                                     first_position_in_string + \
#                                     second_position_in_string + \
#                                     df['Nominal Composition'].iloc[i][space_position + 1:]
#
#                 elif first_position_in_string.isnumeric():
#                     second_position_in_string = df['Nominal Composition'].iloc[i][1]
#
#                     if second_position_in_string.isnumeric():
#                         space_position = df['Nominal Composition'].iloc[i].find(' /')
#                         my_new_string = df['Nominal Composition'].iloc[i][1:space_position] + \
#                                         first_position_in_string + \
#                                         df['Nominal Composition'].iloc[i][space_position + 1:]
#
#                     elif second_position_in_string == ' ':
#                         third_position_in_string = df['Nominal Composition'].iloc[i][2]
#                         if third_position_in_string.isnumeric():
#                             space_position = df['Nominal Composition'].iloc[i].find(' /')
#                             my_new_string = first_position_in_string + \
#                                             df['Nominal Composition'].iloc[i][3:space_position] + \
#                                             third_position_in_string + \
#                                             df['Nominal Composition'].iloc[i][space_position + 1:]
#                         elif third_position_in_string == '-':
#                             fourth_position_in_string = df['Nominal Composition'].iloc[i][4]
#                             space_position = df['Nominal Composition'].iloc[i].find(' /')
#                             my_new_string = first_position_in_string + \
#                                             df['Nominal Composition'].iloc[i][4:space_position] + \
#                                             third_position_in_string + \
#                                             fourth_position_in_string + \
#                                             df['Nominal Composition'].iloc[i][space_position + 1:]
#
#                 df.iloc[i, j] = my_new_string
#
#             if '/ ' in df['Nominal Composition'].iloc[i]:
#                 last_position_in_string = df['Nominal Composition'].iloc[i][-1]
#                 space_position = df['Nominal Composition'].iloc[i].find('/ ')
#                 space_position = space_position + 1
#                 my_new_string = df['Nominal Composition'].iloc[i][:space_position] + \
#                                 last_position_in_string + \
#                                 df['Nominal Composition'].iloc[i][space_position + 1:-1]
#
#                 df.iloc[i, j] = my_new_string
#
#             last_position_in_string = df['Nominal Composition'].iloc[i][-1]
#             if ' /' in df['Nominal Composition'].iloc[i] and last_position_in_string.isnumeric():
#                 space_position = df['Nominal Composition'].iloc[i].find(' /')
#                 my_new_string = df['Nominal Composition'].iloc[i][:space_position] + \
#                                 last_position_in_string + \
#                                 df['Nominal Composition'].iloc[i][space_position + 1:-1]
#
#                 df.iloc[i, j] = my_new_string
#         # rotina para remover espaços sobrando após a rotina de reorganização acima
#         # for i in range(len(df['Nominal Composition'])):
#         #     j = df.columns.get_loc('Nominal Composition')
#         #     if ' ' in df['Nominal Composition'].iloc[i]:
#         #         space_position = df['Nominal Composition'].iloc[i].find(' ')
#         #         my_new_string = df['Nominal Composition'].iloc[i][:space_position] + \
#         #                         df['Nominal Composition'].iloc[i][space_position + 1:]
#         #         df.iloc[i, j] = my_new_string
#     return df
#
#
# def corrigir_composicao_nominal_rfind(df):
#     if "Nominal Composition" in df.columns:
#         for i in range(len(df['Nominal Composition'])):
#             j = df.columns.get_loc('Nominal Composition')
#             if ' /' in df['Nominal Composition'].iloc[i]:
#                 first_position_in_string = df['Nominal Composition'].iloc[i][0]
#                 if first_position_in_string == '–':
#                     second_position_in_string = df['Nominal Composition'].iloc[i][1]
#                     space_position = df['Nominal Composition'].iloc[i].rfind(' /')
#                     my_new_string = df['Nominal Composition'].iloc[i][2:space_position] + \
#                                     first_position_in_string + \
#                                     second_position_in_string + \
#                                     df['Nominal Composition'].iloc[i][space_position + 1:]
#
#                 elif first_position_in_string.isnumeric():
#                     second_position_in_string = df['Nominal Composition'].iloc[i][1]
#
#                     if second_position_in_string.isnumeric():
#                         space_position = df['Nominal Composition'].iloc[i].rfind(' /')
#                         my_new_string = df['Nominal Composition'].iloc[i][1:space_position] + \
#                                         first_position_in_string + \
#                                         df['Nominal Composition'].iloc[i][space_position + 1:]
#
#                     elif second_position_in_string == ' ':
#                         third_position_in_string = df['Nominal Composition'].iloc[i][2]
#                         if third_position_in_string.isnumeric():
#                             space_position = df['Nominal Composition'].iloc[i].rfind(' /')
#                             my_new_string = first_position_in_string + \
#                                             df['Nominal Composition'].iloc[i][3:space_position] + \
#                                             third_position_in_string + \
#                                             df['Nominal Composition'].iloc[i][space_position + 1:]
#                         elif third_position_in_string == '-':
#                             fourth_position_in_string = df['Nominal Composition'].iloc[i][4]
#                             space_position = df['Nominal Composition'].iloc[i].rfind(' /')
#                             my_new_string = first_position_in_string + \
#                                             df['Nominal Composition'].iloc[i][4:space_position] + \
#                                             third_position_in_string + \
#                                             fourth_position_in_string + \
#                                             df['Nominal Composition'].iloc[i][space_position + 1:]
#
#                 df.iloc[i, j] = my_new_string
#
#             if '/ ' in df['Nominal Composition'].iloc[i]:
#                 last_position_in_string = df['Nominal Composition'].iloc[i][-1]
#                 space_position = df['Nominal Composition'].iloc[i].rfind('/ ')
#                 space_position = space_position + 1
#                 my_new_string = df['Nominal Composition'].iloc[i][:space_position] + \
#                                 last_position_in_string + \
#                                 df['Nominal Composition'].iloc[i][space_position + 1:-1]
#
#                 df.iloc[i, j] = my_new_string
#
#             last_position_in_string = df['Nominal Composition'].iloc[i][-1]
#             if ' /' in df['Nominal Composition'].iloc[i] and last_position_in_string.isnumeric():
#                 space_position = df['Nominal Composition'].iloc[i].rfind(' /')
#                 my_new_string = df['Nominal Composition'].iloc[i][:space_position] + \
#                                 last_position_in_string + \
#                                 df['Nominal Composition'].iloc[i][space_position + 1:-1]
#
#                 df.iloc[i, j] = my_new_string
#
#             if ' /' in df['Nominal Composition'].iloc[i] and df['Nominal Composition'].iloc[i].count(' ')==2\
#                     and df['Nominal Composition'].iloc[i][-1]!=' ':
#                 last_space_position = df['Nominal Composition'].iloc[i].rfind(' ')
#                 first_space_position = df['Nominal Composition'].iloc[i].find(' ')
#                 char_after_last_space = df['Nominal Composition'].iloc[i][last_space_position+1]
#                 my_new_string = df['Nominal Composition'].iloc[i][:first_space_position] + \
#                                 char_after_last_space + \
#                                 df['Nominal Composition'].iloc[i][first_space_position + 1:last_space_position] + \
#                                 df['Nominal Composition'].iloc[i][last_space_position + 2:]
#
#                 df.iloc[i, j] = my_new_string
#
#             if ' /' in df['Nominal Composition'].iloc[i] and df['Nominal Composition'].iloc[i].count(' ')>=2:
#                 space_position = df['Nominal Composition'].iloc[i].find(' /')
#                 remainging_string = df['Nominal Composition'].iloc[i][space_position + 1:-1]
#                 next_space = remainging_string.find(' ')
#                 current_char = df['Nominal Composition'].iloc[i][space_position+1+next_space+1]
#                 if current_char.isnumeric():
#                     my_new_string = df['Nominal Composition'].iloc[i][:space_position] + \
#                                     current_char + \
#                                     df['Nominal Composition'].iloc[i][space_position + 1:space_position+1+next_space] +\
#                                     df['Nominal Composition'].iloc[i][space_position+1+next_space+2:]
#                 df.iloc[i, j] = my_new_string
#
#             last_position_in_string = df['Nominal Composition'].iloc[i][-1]
#             penultimate_position_in_string = df['Nominal Composition'].iloc[i][-2]
#             if ' /' in df['Nominal Composition'].iloc[i] and \
#                     last_position_in_string == ' ' and \
#                     penultimate_position_in_string.isnumeric():
#                 space_position = df['Nominal Composition'].iloc[i].rfind(' /')
#                 my_new_string = df['Nominal Composition'].iloc[i][:space_position] + \
#                                 penultimate_position_in_string + \
#                                 df['Nominal Composition'].iloc[i][space_position + 1:-2]
#
#                 df.iloc[i, j] = my_new_string
#
#             if ' /' in df['Nominal Composition'].iloc[i] and \
#                     ' 1-' in df['Nominal Composition'].iloc[i]:
#                 space_position = df['Nominal Composition'].iloc[i].find(' /')
#                 number_position = df['Nominal Composition'].iloc[i][:space_position] + \
#                                 penultimate_position_in_string + \
#                                 df['Nominal Composition'].iloc[i][space_position + 1:-2]
#
#                 df.iloc[i, j] = my_new_string
#         # rotina para remover espaços sobrando após a rotina de reorganização acima
#         # for i in range(len(df['Nominal Composition'])):
#         #     j = df.columns.get_loc('Nominal Composition')
#         #     if ' ' in df['Nominal Composition'].iloc[i]:
#         #         space_position = df['Nominal Composition'].iloc[i].rfind(' ')
#         #         my_new_string = df['Nominal Composition'].iloc[i][:space_position] + \
#         #                         df['Nominal Composition'].iloc[i][space_position + 1:]
#         #         df.iloc[i, j] = my_new_string
#     return df


# entradas para funcao table_reader.Read para cada padrão de pagina
# Read(pdf_path, page,top,left,width,height,columns_spaces,columns_names,clear_table=True):
top, left, width, height, columns_spaces, columns_names, clear_table = [], [], [], [], [], [], []

# INICIO DAS ENTRADAS:
if True:
    # Pg1
    top.append(140)
    left.append(45)
    width.append(486)
    height.append(535)
    columns_spaces.append([19.45, 94.2, 68, 62, 65.3, 39.5, 59.9, 50, 32.7])
    columns_names.append(['Line No.', 'Nominal Composition', 'Product Form', 'Spec. No.', 'Type/Grade',
                          'Desig./UNS No.', 'Class/Condition/Temper', 'Size/Thickness,mm',
                          'Min. Tensile Strength, MPa'])
    clear_table.append(True)

    # Pg2
    top.append(145)
    left.append(63.7)
    width.append(493)
    height.append(515)
    columns_spaces.append(
        [20.5, 27.3, 31.92, 31.92, 31.92, 31.92, 31.92, 31.92, 31.92, 31.92, 31.92, 31.92, 31.92, 31.92, 31.92, 30])
    columns_names.append(['Line No.', 40, 100, 150, 200, 250, 300, 325, 350, 375, 400, 425, 450, 475, 500, 525])
    clear_table.append(True)

    # pg3
    top.append(145)
    left.append(46)
    width.append(495)
    height.append(515)
    columns_spaces.append(
        [19.5, 25.8, 32.16, 32.16, 32.16, 32.16, 32.16, 32.16, 32.16, 32.16, 32.16, 32.16, 32.16, 32.16,
         32.16, 30])
    columns_names.append(['Line No.', 550, 575, 600, 625, 650, 675, 700, 725, 750, 775, 800, 825, 850, 875, 900])
    clear_table.append(True)

    # #pg4
    # top.append(155)
    # left.append(63.7)
    # width.append(495)
    # height.append(511)
    # columns_spaces.append([25, 24.12, 28.32, 28.2, 28.32, 28.2, 28.32, 27.6, 27.72, 27.6, 27.72, 27.6, 27.6, 27.72, 31.56, 27.72,
    #                   27.6])
    # columns_names.append(['Line No.',500, 525, 550, 575, 600, 625, 650, 675, 700, 725, 750, 775, 800, 825, 850, 875, 900])
    # clear_table.append(True)

    pdf_path = "ASME_D_2021.pdf"

    page_start = 620
    page_end = 827

    # page_start = 680
    # page_end = 683

    # Numero da pagina padrão para pular (deixa a lista vazia se nao precisar pular paginas)
    page_skip = [4]
# FIM DAS ENTRADAS

# Chamando procedimento para ler e montar o dataframe
df = Assembly_Table.Read_Table_Complete(pdf_path, page_start, page_end, top, left,
                                        width, height, columns_spaces, columns_names, clear_table, page_skip)

# Aplica o procedimento para corrigir a coluna composição nominal
# df = corrigir_composicao_nominal(df)

# df = corrigir_composicao_nominal_rfind(df)

df.to_csv('ASME_Table_U.csv', sep=';')

pd.set_option("display.max_rows", None, "display.max_columns", None)
print(df)

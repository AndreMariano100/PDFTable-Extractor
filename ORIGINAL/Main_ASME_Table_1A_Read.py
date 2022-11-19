import pandas as pd
import Assembly_Table


#entradas para funcao table_reader.Read para cada padrão de pagina
#Read(pdf_path, page,top,left,width,height,columns_spaces,columns_names,clear_table=True):
top, left, width, height, columns_spaces, columns_names,clear_table=[], [], [], [], [], [],[]

#Pg1
top.append(160)
left.append(50)
width.append(500)
height.append(520)
columns_spaces.append([19, 90, 77, 57, 77.5, 28, 39, 50, 22])
columns_names.append(['Line No.', 'Nominal Composition', 'Product Form', 'Spec. No.', 'Type/Grade',
                           'Desig./UNS No.', 'Class/Condition/Temper', 'Size/Thickness,mm', 'P-No', 'Group No.'])
clear_table.append(True)

#Pg2
top.append(160)
left.append(63.7)
width.append(486)
height.append(511)
columns_spaces.append([19.5, 45.5, 46.8, 42.8, 66.8, 44.6, 29.9, 50.6])
columns_names.append(['Line No.', 'Min. Tensile Strength, MPa', 'Min. Yield Strength, MPa',
                  'Max. Temperature Limits - I','Max. Temperature Limits - III',
                  'Max. Temperature Limits - VIII-1','Max. Temperature Limits - XII',
                  'External Pressure Chart No.','Notes'])
clear_table.append(True)
#pg3

top.append(155)
left.append(45.5)
width.append(500)
height.append(511)
columns_spaces.append([30, 25.92, 32.16, 32.04, 32.16, 32.04, 32.16, 32.16, 32.16, 31.92, 32.16, 32.16, 32.16, 32.04, 32.16])
columns_names.append(['Line No.',40, 65, 100, 125, 150, 200, 250, 300, 325, 350, 375, 400, 425, 450, 475])
clear_table.append(True)


#pg4
top.append(155)
left.append(63.7)
width.append(495)
height.append(511)
columns_spaces.append([25, 24.12, 28.32, 28.2, 28.32, 28.2, 28.32, 27.6, 27.72, 27.6, 27.72, 27.6, 27.6, 27.72, 31.56, 27.72,
                  27.6])
columns_names.append(['Line No.',500, 525, 550, 575, 600, 625, 650, 675, 700, 725, 750, 775, 800, 825, 850, 875, 900])
clear_table.append(True)



pdf_path = "ASME_D_2021.pdf"

page_start = 60
page_end = 211

#Numero da pagina padrão para pular- deixar vazio se nao eh para pular
page_skip = []



df = Assembly_Table.Read_Table_Complete(pdf_path, page_start, page_end,top,left,width,height,columns_spaces,columns_names,clear_table, page_skip)

# Corrige coluna "Nominal Composition"
if "Nominal Composition" in df.columns:
    for i in range(len(df['Nominal Composition'])):
        j = df.columns.get_loc('Nominal Composition')
        if ' /' in df['Nominal Composition'].iloc[i]:
            first_position_in_string = df['Nominal Composition'].iloc[i][0]
            if first_position_in_string == '–':
                second_position_in_string = df['Nominal Composition'].iloc[i][1]
                space_position = df['Nominal Composition'].iloc[i].find(' ')
                my_new_string = df['Nominal Composition'].iloc[i][2:space_position] +\
                                first_position_in_string +\
                                second_position_in_string +\
                                df['Nominal Composition'].iloc[i][space_position+1:]

            elif first_position_in_string.isnumeric():
                space_position = df['Nominal Composition'].iloc[i].find(' ')
                my_new_string = df['Nominal Composition'].iloc[i][1:space_position] + \
                                first_position_in_string + \
                                df['Nominal Composition'].iloc[i][space_position+1:]

            df.iloc[i,j] = my_new_string

        if '/ ' in df['Nominal Composition'].iloc[i]:
            last_position_in_string = df['Nominal Composition'].iloc[i][-1]
            space_position = df['Nominal Composition'].iloc[i].find(' ')
            my_new_string = df['Nominal Composition'].iloc[i][:space_position] + \
                            last_position_in_string + \
                            df['Nominal Composition'].iloc[i][space_position + 1:-1]

            df.iloc[i, j] = my_new_string

df.to_csv('ASME_Table_1A.csv',sep=';')

pd.set_option("display.max_rows", None, "display.max_columns", None)
print(df)
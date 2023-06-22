import math
import numpy as np
shear_dia_list = [12, 16, 20, 25]
shear_spacing_list = [100, 150, 200, 250]

#create a function which returns the count of rebar per beam width (dimensionless). 
#takes int and returns int
def rebar_count(width):
    rebar_string = str(width)
    rebar_final_count = int(rebar_string[0])
    if rebar_final_count == 2:
        return rebar_final_count
    else:
        return rebar_final_count - 1

#create a function which assess whether side face rebar for torsion is required.
def side_face_assessment(df, column_a, column_b, column_c, column_d):
    df.loc[df[column_b] > 0, column_c] = np.ceil((df[column_b] / 2) + df[column_c])
    df.loc[df[column_b] > 0, column_d] = np.ceil((df[column_b] / 2) + df[column_d])
    df.loc[df[column_a] > 600, column_c] = np.ceil(df[column_c] - (df[column_b] / 2))
    df.loc[df[column_a] > 600, column_d] = np.ceil(df[column_d] - (df[column_b] / 2))
    df.loc[df[column_a] <= 600, column_b] = 'Side face reinforcement is not required'
    return df


#create a function which assess how many legs to provide depending on count of rebar. 
#takes int and returns int. 
#this function assumes that the width of the beam is not greater than 2 metres
def shear_legs(rebar_count):
    if rebar_count <= 2 or rebar_count < 4:
        return 2
    elif rebar_count >= 4 and rebar_count < 6:
        return 4
    elif rebar_count >= 6 and rebar_count < 10:
        return 6
    elif rebar_count >= 11:
        return 8

# this function checks the value in the df cell and loops a list until the value exceeds it
# it then replaces the cell value with a string
def rebar_string(row, column_a, column_b):
    dia_list = [16, 20, 25, 32]
    rebar_string = ''
    for dia in dia_list:
        if np.floor(np.pi * (dia / 2)**2) * row[column_a] > row[column_b]:
            rebar_string = f'{row[column_a]}T{dia}'
            break  # stop looping once we found a match
        elif np.floor(np.pi * (dia / 2)**2) * row[column_a] * 2 > row[column_b]:
            rebar_string = f'2 rows of {row[column_a]}T{dia}'
            break  # stop looping once we found a match
        elif np.floor(np.pi * (dia / 2)**2) * row[column_a] * 3 > row[column_b]:
            rebar_string = f'3 rows of {row[column_a]}T{dia}'
            break  # stop looping once we found a match
    return rebar_string

# this function does the exact same thing as rebar_string, but returns the total area in mm2.
def rebar_area(row, column_a, column_b):
    dia_list = [16, 20, 25, 32]
    rebar_area = 0
    f = lambda x: np.floor(np.pi * (x / 2)**2) * row[column_a]
    for dia in dia_list:
        if f(dia) > row[column_b]:
            rebar_area = f(dia)
            break
        elif f(dia) * 2 > row[column_b]:
            rebar_area = f(dia) * 2
            break
        elif f(dia) * 3 > row[column_b]:
            rebar_area = f(dia) * 3
            break
    return rebar_area

#this function subtracts the provided by the needed to provide the residual.
def residual_rebar(row, column_a, column_b, column_c, column_d):
    bottom_residual = row[column_a] - row[column_b]
    top_residual = row[column_c] - row[column_d]
    return bottom_residual + top_residual

#this function creates a column to check the clear depth for the side face reinforcement
#it assumes a shear dia of 12mm, longitudinal dia of 20mm, and a cover of 25mm
def side_face_count(depth):
    side_clear_space = depth - (2*25) - (2*12) - 20
    return math.floor(side_clear_space)

# this function checks the value in the df cell and loops until side face reinforcement is met
# assuming it is needed, if it isnt it breaks.
def side_face_reinf(row, column_a, column_b, column_c):
    spacing_list = [250, 200, 150]
    dia_list = [16, 20, 25, 32]
    f = lambda x, y: float(round(row[column_b] / x)) * float((np.pi*(y / 2)**2)) - float(row[column_c])
    spacing_string = ''
    if row[column_a] != 'Side face reinforcement is not required':
        for spacing in spacing_list:
            for dia in dia_list:
                if f(spacing, dia) > float(row[column_a]):
                    spacing_string = f'T{dia}@{spacing} EF'
                    break
            else:
                continue
            break
    else:
        return 'Not needed'
    return spacing_string



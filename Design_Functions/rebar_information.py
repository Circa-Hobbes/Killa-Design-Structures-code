import math
import numpy as np


# create a function which returns the count of rebar per beam width (dimensionless).
# takes int and returns int
def rebar_count(width):
    rebar_final_count = width // 100
    if rebar_final_count == 2:
        return rebar_final_count
    else:
        return rebar_final_count - 1


# create a function which assess whether side face rebar for torsion is required.
# def side_face_assessment(df, depth, tor_rebar, bot_rebar, top_rebar):
#     df = df.fillna(0)
#     df.loc[df[tor_rebar] > 0, bot_rebar] = np.ceil((df[tor_rebar] / 2) + df[bot_rebar])
#     df.loc[df[tor_rebar] > 0, top_rebar] = np.ceil((df[tor_rebar] / 2) + df[top_rebar])
#     df.loc[df[depth] > 600, bot_rebar] = np.ceil(df[bot_rebar] - (df[tor_rebar] / 2))
#     df.loc[df[depth] > 600, top_rebar] = np.ceil(df[top_rebar] - (df[tor_rebar] / 2))
#     # df.loc[df[depth] <= 600, tor_rebar] = "Side face reinforcement is not required"
#     return df


def add_long_rebar(df, column_a, column_b, column_c, column_d):
    df = df.fillna(0)
    condition1 = df[column_a] <= 600
    df.loc[condition1, column_c] = np.ceil(
        (df.loc[condition1, column_b] / 2) + df.loc[condition1, column_c]
    )
    df.loc[condition1, column_d] = np.ceil(
        (df.loc[condition1, column_b] / 2) + df.loc[condition1, column_d]
    )
    # condition2 = df[column_a] > 600
    # df.loc[condition2, column_c] = np.ceil(
    #     df.loc[condition2, column_c] - (df.loc[condition2, column_b] / 2)
    # )
    # df.loc[condition2, column_d] = np.ceil(
    #     df.loc[condition2, column_d] - (df.loc[condition2, column_b] / 2)
    # )
    # condition3 = df[column_a] <= 600
    # df.loc[condition3, column_b] = "Side face reinforcement is not required"
    return df


# create a function which assess how many legs to provide depending on count of rebar.
# takes int and returns int.
# this function assumes that the width of the beam is not greater than 2 metres

# NOT USED
# def shear_legs(rebar_count):
#     if rebar_count <= 2 or rebar_count < 4:
#         return 2
#     elif rebar_count >= 4 and rebar_count < 6:
#         return 4
#     elif rebar_count >= 6 and rebar_count < 10:
#         return 6
#     elif rebar_count >= 11:
#         return 8


# this function checks the value in the df cell and loops a list until the value exceeds
# it. it then replaces the cell value with a string
def rebar_string(row, column_a, column_b, column_c):
    dia_list = [16, 20, 25, 32]
    rebar_string = ""

    if row[column_c] == "False":
        for dia_1 in dia_list:
            if np.floor(np.pi * (dia_1 / 2) ** 2) * row[column_a] > row[column_b]:
                rebar_string = f"{row[column_a]}T{dia_1}"
                break  # stop looping once we found a match
            for dia_2 in dia_list:
                if (
                    np.floor(np.pi * (dia_1 / 2) ** 2) * row[column_a]
                    + np.floor(np.pi * (dia_2 / 2) ** 2) * row[column_a]
                    > row[column_b]
                ):
                    rebar_string = f"{row[column_a]}T{dia_1} + {row[column_a]}T{dia_2}"
                    break  # stop looping once we found a match
            # elif np.floor(np.pi * (dia / 2) ** 2) * row[column_a] * 3 > row[column_b]:
            #     rebar_string = f"{row[column_a]}T{dia} + {row[column_a]}T{dia} + {row[column_a]}T{dia}"
            #     break  # stop looping once we found a match
        return rebar_string
    # elif row[column_d] == "False":
    #     for dia in dia_list:
    #         if np.floor(np.pi * (dia / 2) ** 2) * row[column_a] > row[column_b]:
    #             rebar_string = f"{row[column_a]}T{dia}"
    #             break  # stop looping once we found a match
    #         elif np.floor(np.pi * (dia / 2) ** 2) * row[column_a] * 2 > row[column_b]:
    #             rebar_string = f"{row[column_a]}T{dia} + {row[column_a]}T{dia}"
    #             break  # stop looping once we found a match
    #         elif np.floor(np.pi * (dia / 2) ** 2) * row[column_a] * 3 > row[column_b]:
    #             rebar_string = f"{row[column_a]}T{dia} + {row[column_a]}T{dia} + {row[column_a]}T{dia}"
    #             break  # stop looping once we found a match
    #     return rebar_string
    if not rebar_string:
        return "Inc. rebar count and re-assess."
    else:
        return "Overstressed. Please re-assess"


# this function does the exact same thing as rebar_string but returns the total area
def rebar_area(row, column_a, column_b, column_c):
    dia_list = [16, 20, 25, 32]
    rebar_area = 0
    if row[column_c] == "False":
        f = lambda x: np.floor(np.pi * (x / 2) ** 2) * row[column_a]
        for dia_1 in dia_list:
            if f(dia_1) > row[column_b]:
                rebar_area = f(dia_1)
                break
            for dia_2 in dia_list:
                if f(dia_1) + f(dia_2) > row[column_b]:
                    rebar_area = f(dia_1) + f(dia_2)
                break
            # elif f(dia) * 2 > row[column_b]:
            #     rebar_area = f(dia) * 2
            #     break
            # elif f(dia) * 3 > row[column_b]:
            #     rebar_area = f(dia) * 3
            #     break
        return rebar_area
    # elif row[column_d] == "False":
    #     f = lambda x: np.floor(np.pi * (x / 2) ** 2) * row[column_a]
    #     for dia in dia_list:
    #         if f(dia) > row[column_b]:
    #             rebar_area = f(dia)
    #             break
    #         elif f(dia) * 2 > row[column_b]:
    #             rebar_area = f(dia) * 2
    #             break
    #         elif f(dia) * 3 > row[column_b]:
    #             rebar_area = f(dia) * 3
    #             break
    else:
        return "Overstressed. Please re-assess"


# this function subtracts the provided by the needed to provide the residual.
def residual_rebar(row, column_a, column_b, column_c, column_d):
    if (
        row[column_a] == "Overstressed. Please re-assess"
        or row[column_c] == "Overstressed. Please re-assess"
    ):
        return "Overstressed. Please re-assess"
    else:
        bottom_residual = row[column_a] - row[column_b]
        top_residual = row[column_c] - row[column_d]
        return bottom_residual + top_residual


# this function creates a column to check the clear depth for the side reinforcement
# it assumes a shear dia of 12mm, longitudinal dia of 20mm, and a cover of 40mm
def side_face_count(depth):
    side_clear_space = depth - (2 * 40) - (2 * 12) - (2 * 20)
    return math.floor(side_clear_space)


# checks the value in the df cell and loops until side reinforcement is met
# assuming it is needed, if it isnt it breaks.
def side_face_reinf(row, column_a, column_b, column_c, column_d):
    spacing_list = [250, 200, 150]
    dia_list = [12, 16, 20, 25, 32]
    if row[column_d] == "False" and row[column_c] != "Overstressed. Please re-assess":
        f = lambda x, y: np.floor(2 * (row[column_b] / x)) * (np.pi * (y / 2) ** 2)
        spacing_string = ""
        if row[column_a] != 0:
            for dia in dia_list:
                for spacing in spacing_list:
                    if f(spacing, dia) > row[column_a] - row[column_c]:
                        spacing_string = f"T{dia}@{spacing} EF"
                        break
                else:
                    continue
                break
        else:
            return "Not needed"
        return spacing_string
    else:
        return "Overstressed. Please re-assess"


def side_face_area(row, column_a, column_b, column_c, column_d):
    """returns the area of side face reinforcement provided in mm2

    Args:
        row (_type_): v6_flexural_df
        column_a (_type_): required longitudinal torsion rebar
        column_b (_type_): side face clear depth (mm)
        column_c (_type_): the residual rebar to subtract required torsion rebar
        column_d (_type_): to check if shear is overstressed
    """
    spacing_list = [250, 200, 150]
    dia_list = [12, 16, 20, 25, 32]
    if row[column_d] == "False" and row[column_c] != "Overstressed. Please re-assess":
        f = lambda x, y: np.floor(2 * (row[column_b] / x)) * (np.pi * (y / 2) ** 2)
        spacing_area = 0
        if row[column_a] != 0:
            for dia in dia_list:
                for spacing in spacing_list:
                    if f(spacing, dia) > row[column_a] - row[column_c]:
                        spacing_area = np.floor(f(spacing, dia))
                        break
                else:
                    continue
                break
        else:
            return "Not needed"
        return spacing_area
    else:
        return "Overstressed. Please re-assess"


# this function returns the total shear area required to satisfy
def shear_area_req(row, column_a, column_b):
    required = 0
    if row[column_a] == "O/S":
        required = "Overstressed. Please re-assess"
    else:
        required = row[column_a] + 2 * row[column_b]
    return required


# this function returns the total shear legs based on the width of the beam
# column_a is the width and column_b is depth, column_c is required shear area
# assumes fc = 45 mpa
def req_legs(column_a):
    leg = 0
    if column_a < 400:
        leg = 2
    elif column_a >= 400 and column_a < 800:
        leg = 4
    elif column_a >= 800:
        leg = 6
    return leg


# this function loops through dia's and spacing to meet the required shear area
# x = spacing, y = dia for lambda function
def shear_string(row, column_a, column_b):
    shear_dia_list = [12, 16, 20, 25]
    shear_spacing_list = [250, 200, 150, 100]
    shear_string = ""
    legs = row[column_a]

    if row[column_b] != "Overstressed. Please re-assess":
        for dia in shear_dia_list:
            for spacing in shear_spacing_list:
                if (1000 / spacing) * (np.pi * (dia / 2) ** 2) * legs > row[column_b]:
                    shear_string = f"{legs}L-T{dia}@{spacing}"
                    break
            if (
                shear_string
            ):  # If shear_string is assigned, break the outer loop as well.
                break
        return shear_string
    else:
        return "Overstressed. Please reassess"


def shear_area(row, column_a, column_b):
    """loops through dias and spacing to meet required shear area

    Args:
        row (_type_): v2_shear_df row
        column_a (_type_): required shear legs
        column_b (_type_): required shear area
        column_c (_type_): shear rebar area

    Returns:
        _type_: returns the area of shear in mm2
    """
    shear_dia_list = [12, 16, 20, 25]
    shear_spacing_list = [250, 200, 150, 100]
    area = 0
    legs = row[column_a]
    if row[column_b] != "Overstressed. Please re-assess":
        for dia in shear_dia_list:
            for spacing in shear_spacing_list:
                if (1000 / spacing) * (np.pi * (dia / 2) ** 2) * legs > row[column_b]:
                    area = round((1000 / spacing) * (np.pi * (dia / 2) ** 2) * legs)
                    break
            if area:  # If shear_string is assigned, break the outer loop as well.
                break
        return area
    else:
        return "Overstressed. Please reassess"


# this function cleans the cell of unnamed: 3 column to provide the width of each beam.
def clean_width_dimensions(width):
    width_list = list(width)  # turn string into list of individual indexes
    width_list = [
        el.lower() for el in width_list
    ]  # use list comprehension to turn list into lower case values
    excluded_values = [
        "p",
        "t",
        "b",
        "-",
        "_",
        "c",
        "/",
    ]  # create list of excluded indices
    v1_width_list = [
        ex for ex in width_list if ex not in excluded_values
    ]  # use list comprehension to return list excluding indices
    index_list = v1_width_list.index(
        "x"
    )  # index the list to x to retrieve required width
    v2_width_list = v1_width_list[:index_list]  # slice the width list to the index x
    true_width = "".join(v2_width_list)  # join the list into a string
    return int(true_width)  # turn string into int so it can be used in other functions


# this function cleans the cell of unnamed: 3 column to provide the depth of each beam.
# this function follows the same steps as clean_width_dimensions function
def clean_depth_dimensions(depth):
    depth_list = list(depth)
    depth_list = [el.lower() for el in depth_list]
    excluded_values = ["p", "t", "b", "-", "_", "c", "/"]
    v1_depth_list = [ex for ex in depth_list if ex not in excluded_values]
    index_list = v1_depth_list.index("x")
    v2_depth_list = v1_depth_list[1 + index_list : -4]
    true_depth = "".join(v2_depth_list)
    return int(true_depth)


def flex_overstressed_check(row, column_a, column_b):
    """This function checks if either flexural combinations are overstressed
    if False, it's not overstressed and therefore can continue designing
    if True, its overstressed and all consequent calculations may be ignored
    Args:
        row (_type_): the row considered in the df
        column_a (_type_): the first design combo
        column_b (_type_): the second design combo
    """
    if row[column_a] == "O/S":
        return "True"
    elif row[column_b] == "O/S":
        return "True"
    else:
        return "False"


def shear_overstressed_check(row, column_a):
    """This function checks if the shear combination is overstressed
    if False, it's not overstressed and therefore can continue designing
    if True, its overstressed and all consequent calculations may be ignored
    Args:
        row (_type_): row considered in the df
        column_a (_type_): shear design combination being assessed
    """
    if row[column_a] == "O/S":
        return "True"
    else:
        return "False"


def quick_side_check(row, column_a, column_b):
    """if the side face reinforcement is less than 600 depth, return not needed

    Args:
        row (Series): row of beam_schedule_final_df
        column_a (tuple): dimensions, depth
        column_b (tuple): side face reinforcement, empty sub
    """
    sub_a, sub_b = column_a[1], column_b[1]
    column_a, column_b = column_a[0], column_b[0]

    if row[column_b, sub_b] == "Overstressed. Please reassess":
        pass
    elif row[column_a, sub_a] <= 600:
        row[column_b, sub_b] = " "


def torsion_check(row, column_a, column_b, column_c):
    """checks if outer two legs can withstand torsion

    Args:
        row (_type_): df
        column_a (_type_): width
        column_b (_type_): shear reinforcement provided
        column_c (_type_): shear torsion requirement

    Returns:
        _type_: _description_
    """
    check = ""
    if row[column_b] == "Overstressed. Please reassess":
        check = "Overstressed. Please reassess"
    else:
        if row[column_a] < 400:
            if row[column_b] > row[column_c]:
                check = "OK"
            else:
                check = "FAIL"
        elif row[column_a] >= 400 and row[column_a] < 800:
            if row[column_b] / 4 > row[column_c]:
                check = "OK"
            else:
                check = "FAIL"
        elif row[column_a] >= 800:
            if row[column_b] / 6 > row[column_c]:
                check = "OK"
            else:
                check = "FAIL"
    return check


# create a function to handle strings and integers in a group
def handle_group(g):
    # check if the group contains any strings
    strings = g[g.apply(lambda x: isinstance(x, str))]
    if not strings.empty:
        # if there are strings, return the first string
        return strings.iloc[0]
    else:
        # if there are no strings, return the max value
        return g.max()

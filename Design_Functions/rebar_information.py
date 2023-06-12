import math
dia_list = [16, 20, 25, 32]
shear_dia_list = [12, 16, 20, 25]
shear_spacing_list = [100, 150, 200, 250]

#create a function which calculates the area of rebar in mm^2. 
#takes int and returns int
def dia_area_calc(diameter):
    return math.floor(math.pi * (diameter / 2)**2)

#create a function which returns the count of rebar per beam width (dimensionless). 
#takes int and returns int
def rebar_count(width):
    rebar_string = str(width)
    rebar_final_count = int(rebar_string[0])
    if rebar_final_count == 2:
        return rebar_final_count
    else:
        return rebar_final_count - 1

#create a function which assess whether side face rebar for tension is required. 
#takes int and returns boolean.
#true means required, false means not required.
def side_face_assessment(depth):
    if depth > 600:
        return True
    else:
        return False

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

#create a function which multiplies the area of rebar by the count of rebar provided.
#takes int and returns int.
def rebar_area_provided(dia_area_calc, rebar_count):
    return math.floor(dia_area_calc * rebar_count)

#create a function which takes a required area of rebar and checks if the provided rebar is greater than it. 
#if it reaches the end of the list, then it prints 'another layer required', and multiplies provided rebar area by 2.
def flexural_rebar_check(rebar_area_provided, rebar_area_required):
    rebar_area_required = 1234
    for i in dia_list:
        if rebar_area_provided(dia_area_calc(i), rebar_count(400)) > rebar_area_required:
            return f'{rebar_count(400)}T{i}'
        else:
            return 
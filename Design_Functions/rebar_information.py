import math
dia_array = [16, 20, 25, 32]

#create a function which calculates the area of rebar in mm^2. takes int and returns int
def diam_area_calc(diameter):
    return math.floor(math.pi * (diameter / 2)**2)

#create a function which returns the count of rebar per beam width (dimensionless). takes int and returns int
def rebar_count(width):
    
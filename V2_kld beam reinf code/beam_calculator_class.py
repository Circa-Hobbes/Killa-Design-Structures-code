import math
import numpy as np
import pandas as pd


class Beam:
    """This class aims to obtain the necessary information to calculate the beam
    reinforcement schedule.
    """

    def __init__(
        self,
        id,
        width,
        depth,
        pos_flex_combo,
        neg_flex_combo,
        req_top_flex_reinf,
        req_bot_flex_reinf,
        req_flex_torsion_reinf,
        shear_combo,
        torsion_combo,
        req_shear_reinf,
        req_torsion_reinf,
    ):
        """Begin by initializing attributes that define the makeup of a reinforced
        concrete beam.
        """
        self.id = id
        self.width = width
        self.depth = depth
        self.pos_flex_combo = pos_flex_combo
        self.neg_flex_combo = neg_flex_combo
        self.req_top_flex_reinf = req_top_flex_reinf
        self.req_bot_flex_reinf = req_bot_flex_reinf
        self.req_flex_torsion_reinf = req_flex_torsion_reinf
        self.shear_combo = shear_combo
        self.torsion_combo = torsion_combo
        self.req_shear_reinf = req_shear_reinf
        self.req_torsion_reinf = req_torsion_reinf
        self.flex_rebar_count = None
        self.flex_top_left_rebar_string = None
        self.flex_top_middle_rebar_string = None
        self.flex_top_right_rebar_string = None
        self.flex_bot_left_rebar_string = None
        self.flex_bot_middle_rebar_string = None
        self.flex_bot_right_rebar_string = None

    def __str__(self):
        """Create a string describing the attributes of each instantiated beam.

        Returns:
            _type_: A string of the attributes of a beam.
        """
        return f"""ETABS Beam ID: {self.id}

Width: {self.width} mm 
Depth: {self.depth} mm

Positive Flexural Combo: {self.pos_flex_combo}
Negative Flexural Combo: {self.neg_flex_combo}

Required Top Flexural Reinforcement: {self.req_top_flex_reinf} mm^2
Required Bottom Flexural Reinforcement: {self.req_bot_flex_reinf} mm^2
Required Flexural Torsion Reinforcement: {self.req_flex_torsion_reinf} mm^2

Shear Combo: {self.shear_combo}
Torsion Combo: {self.torsion_combo}

Required Shear Reinforcement: {self.req_shear_reinf} mm^2/m
Required Torsion Reinforcement: {self.req_torsion_reinf} mm^2/m

Calculated Longitudinal Rebar Count: {self.flex_rebar_count}
Provided Longitudinal Top Left Reinforcement: {self.flex_top_left_rebar_string}
Provided Longitudinal Top Middle Reinforcement: {self.flex_top_middle_rebar_string}
Provided Longitudinal Top Right Reinforcement: {self.flex_top_right_rebar_string}

Provided Longitudinal Bottom Left Reinforcement: {self.flex_bot_left_rebar_string}
Provided Longitudinal Bottom Middle Reinforcement: {self.flex_bot_middle_rebar_string}
Provided Longitudinal Bottom Right Reinforcement: {self.flex_bot_right_rebar_string}"""

    @staticmethod
    def get_width(width):
        """This function cleans and retrieves the relevant width of the beam.

        Args:
            width (int): Width in column of dataframe to clean and get width of beam.
        """
        width_list = list(width)
        width_list = [el.lower() for el in width_list]
        excluded_values = [
            "p",
            "t",
            "b",
            "-",
            "_",
            "c",
            "/",
        ]
        v1_width_list = [ex for ex in width_list if ex not in excluded_values]
        index_list = v1_width_list.index("x")
        v2_width_list = v1_width_list[:index_list]
        true_width = "".join(v2_width_list)
        return int(true_width)

    @staticmethod
    def get_depth(depth):
        """This function cleans and retrives the relevant depth of the beam.

        Args:
            depth (int): the Integer depth in column of dataframe to clean and get depth of beam.
        """
        depth_list = list(depth)
        depth_list = [el.lower() for el in depth_list]
        excluded_values = ["p", "t", "b", "-", "_", "c", "/"]
        v1_depth_list = [ex for ex in depth_list if ex not in excluded_values]
        index_list = v1_depth_list.index("x")
        v2_depth_list = v1_depth_list[1 + index_list : -4]
        true_depth = "".join(v2_depth_list)
        return int(true_depth)

    @staticmethod
    def check_combo(combo_list):
        """This function checks if any of the flexural combos in the list is overstressed.

        Args:
            combo_list (list of string): Checks each flexural combo in the list.

        Returns:
            list of string: Returns "True" for each overstressed combo and "False" for each not overstressed.
        """
        return ["True" if combo == "O/S" else "False" for combo in combo_list]

    def get_long_count(self):
        """This method takes a defined instance and calculates the required longitudinal rebar count based on its width.

        Returns:
            int: The integer count is attributed to the instance. If it's greater than 2, it's subtracted by one. Else, it's 2.
        """
        self.flex_rebar_count = self.width // 100
        if self.flex_rebar_count > 2:
            self.flex_rebar_count -= 1
        else:
            self.flex_rebar_count = 2
        return self.flex_rebar_count

    def flex_torsion_splitting(self):
        """This method assess the depth of the beam. If the depth is > 600mm, it exits the method.
        If it's <=600mm, it takes the torsion flexural requirement list, splits each index into two,
        and then distributes it amongst the top and bottom longitudinal reinforcement. It modifies
        the attributes in place and changes the flex_torsion reinforcement to a list of 0's.
        """
        if self.depth <= 600:
            divided_torsion_list = [i / 2 for i in self.req_flex_torsion_reinf]
            self.req_top_flex_reinf = [
                a + b for a, b in zip(divided_torsion_list, self.req_top_flex_reinf)
            ]
            self.req_bot_flex_reinf = [
                a + b for a, b in zip(divided_torsion_list, self.req_bot_flex_reinf)
            ]
            self.req_flex_torsion_reinf = [0, 0, 0]

    def get_top_flex_rebar_string(self):
        """This method loops through the required top flexural reinforcement and provides a string
        containing the schedule for each part of the beam. Once the string has been made, the schedule
        for each section of the beam is indexed to its relevant attribute."""
        dia_list = [16, 20, 25, 32]
        target = self.req_top_flex_reinf.copy()
        if self.neg_flex_combo == "False":
            for index, req in enumerate(target):
                for dia_1 in dia_list:
                    if np.floor(np.pi * (dia_1 / 2) ** 2) * self.flex_rebar_count > req:
                        target[index] = f"{self.flex_rebar_count}T{dia_1}"
                        break
                    for dia_2 in dia_list:
                        if (
                            np.floor(np.pi * (dia_1 / 2) ** 2) * self.flex_rebar_count
                            + np.floor(np.pi * (dia_2 / 2) ** 2) * self.flex_rebar_count
                            > req
                        ):
                            target[
                                index
                            ] = f"{self.flex_rebar_count}T{dia_1} + {self.flex_rebar_count}T{dia_2}"
                            break
                for index, item in enumerate(target):
                    if item == "":
                        target[index] = "Increase rebar count or re-assess"
        else:
            target = ["Overstressed. Please re-assess"] * len(target)
        self.flex_top_left_rebar_string = target[0]
        self.flex_top_middle_rebar_string = target[1]
        self.flex_top_right_rebar_string = target[2]

    def get_bot_flex_rebar_string(self):
        """This method loops through the required bottom flexural reinforcement and provides a string
        containing the schedule for each part of the beam. Once the string has been made, the schedule
        for each section of the beam is indexed to its relevant attribute.
        """
        dia_list = [16, 20, 25, 32]
        target = self.req_bot_flex_reinf.copy()
        if self.pos_flex_combo == "False":
            for index, req in enumerate(target):
                for dia_1 in dia_list:
                    if np.floor(np.pi * (dia_1 / 2) ** 2) * self.flex_rebar_count > req:
                        target[index] = f"{self.flex_rebar_count}T{dia_1}"
                        break
                    for dia_2 in dia_list:
                        if (
                            np.floor(np.pi * (dia_1 / 2) ** 2) * self.flex_rebar_count
                            + np.floor(np.pi * (dia_2 / 2) ** 2) * self.flex_rebar_count
                            > req
                        ):
                            target[
                                index
                            ] = f"{self.flex_rebar_count}T{dia_1} + {self.flex_rebar_count}T{dia_2}"
                            break
                for index, item in enumerate(target):
                    if item == "":
                        target[index] = "Increase rebar count or re-assess"
        else:
            target = ["Overstressed. Please re-assess"] * len(target)
        self.flex_bot_left_rebar_string = target[0]
        self.flex_bot_middle_rebar_string = target[1]
        self.flex_bot_right_rebar_string = target[2]

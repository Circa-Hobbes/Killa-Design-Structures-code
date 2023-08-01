import math
import numpy as np
import pandas as pd


class Beam:
    """This class aims to obtain the necessary information to calculate the beam
    reinforcement schedule.
    """

    def __init__(
        self,
        df,
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
        self.df = df.loc[df["Unnamed: 1"] == id]
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

    def __str__(self):
        """Create a string describing the attributes of each instantiated beam.

        Returns:
            _type_: A string of the attributes of a beam.
        """
        return f"""ETABS Beam ID: {self.id}
Width: {self.width}mm 
Depth: {self.depth}mm
Positive Flexural Combo: {self.pos_flex_combo}
Negative Flexural Combo: {self.neg_flex_combo}
Required Top Flexural Reinforcement: {self.req_top_flex_reinf}mm^2
Required Bottom Flexural Reinforcement: {self.req_bot_flex_reinf}mm^2
Required Flexural Torsion Reinforcement: {self.req_flex_torsion_reinf}mm^2
Shear Combo: {self.shear_combo}
Torsion Combo: {self.torsion_combo}
Required Shear Reinforcement: {self.req_shear_reinf}mm^2/m
Required Torsion Reinforcement: {self.req_torsion_reinf}mm^2/m"""

    @staticmethod
    def get_width(width):
        """This function cleans and retrieves the relevant width of the beam.

        Args:
            width (_type_): Width in column of dataframe to clean and get width of beam.
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
            depth (_type_): Depth in column of dataframe to clean and get depth of beam.
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

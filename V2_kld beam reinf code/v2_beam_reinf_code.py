# import Design_Functions.rebar_information as rebar_func
from beam_calculator_class import Beam
import pandas as pd

# import importlib
import numpy as np
import tkinter as tk

# import sys
import importlib
from tkinter.filedialog import askopenfilename, asksaveasfilename


# Create all instances, i.e. etabs id's of the Beam class when the script is run.
def create_instance(df, id, width, depth, pos_flex_combo, neg_flex_combo):
    beam = Beam(df, id, width, depth, pos_flex_combo, neg_flex_combo)
    return beam


# Create function to import ETABS beam design extraction spreadsheet.
def import_file():
    root = tk.Tk()
    root.withdraw()
    filepath = askopenfilename()
    root.destroy()
    return filepath


# Call import_file function and associate spreadsheet to variable.
excel_file = import_file()

# Initialise first flexural and shear dataframes.
initial_flexural_df = pd.read_excel(excel_file, sheet_name=0)
initial_shear_df = pd.read_excel(excel_file, sheet_name=1)

# Remove the first two rows of both dataframes.
initial_flexural_df = initial_flexural_df.drop([0, 1])
initial_shear_df = initial_shear_df.drop([0, 1])

# Reset indices in place for easier manipulation.
initial_flexural_df = initial_flexural_df.reset_index(drop=True)
initial_shear_df = initial_shear_df.reset_index(drop=True)

# Begin manipulation and cleaning of dataframe
if __name__ == "__main__":
    # Slice through the flexural df and get the etabs id.
    e_ids = initial_flexural_df["Unnamed: 1"].iloc[::3]

    # Slice through the flexural df and get the cleaned width.
    beam_widths = initial_flexural_df["Unnamed: 3"].iloc[::3].apply(Beam.get_width)

    # Slice through the flexural df and get the cleaned depth.
    beam_depths = initial_flexural_df["Unnamed: 3"].iloc[::3].apply(Beam.get_depth)

    # Take each beam's positive flexural combo and put it in a list within a list.
    positive_combo_list = initial_flexural_df["Unnamed: 9"].tolist()
    nested_pos_combo_list = [
        positive_combo_list[i : i + 3] for i in range(0, len(positive_combo_list), 3)
    ]
    # Repeat same process as positive flexural combo for negative flexural combo.
    negative_combo_list = initial_flexural_df["Unnamed: 6"].tolist()
    nested_neg_combo_list = [
        negative_combo_list[i : i + 3] for i in range(0, len(negative_combo_list), 3)
    ]

    # Take the nested list and return OK or O/S as a string in a list.
    nested_pos_combo_list = [
        "O/S"
        if any(str(element).strip().lower() in ["o/s", "nan"] for element in sublist)
        else "OK"
        for sublist in nested_pos_combo_list
    ]
    nested_neg_combo_list = [
        "O/S"
        if any(str(element).strip().lower() in ["o/s", "nan"] for element in sublist)
        else "OK"
        for sublist in nested_neg_combo_list
    ]

    # Slice through the flexural df and retrieve whether is it overstressed in positive combo.
    positive_flex_combo = Beam.check_flex_combo(nested_pos_combo_list)

    # Slice through the flexural df and retrieve whether it is overstressed in negative combo.
    negative_flex_combo = Beam.check_flex_combo(nested_neg_combo_list)

    # Call create_instance function and create instances of all etabs ids.
    beam_instances = [
        create_instance(
            initial_flexural_df, e_id, width, depth, pos_flex_combo, neg_flex_combo
        )
        for e_id, width, depth, pos_flex_combo, neg_flex_combo in zip(
            e_ids, beam_widths, beam_depths, positive_flex_combo, negative_flex_combo
        )
    ]

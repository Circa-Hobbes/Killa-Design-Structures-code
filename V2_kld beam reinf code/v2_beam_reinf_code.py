# import Design_Functions.rebar_information as rebar_func
from beam_calculator_class import Beam
import pandas as pd

# import importlib
import numpy as np
import tkinter as tk

# import sys
import importlib
from tkinter.filedialog import askopenfilename, asksaveasfilename


# Create all instances of Beam class.
def create_instance(
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
    beam = Beam(
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
    )
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
    positive_flex_combo = Beam.check_combo(nested_pos_combo_list)

    # Slice through the flexural df and retrieve whether it is overstressed in negative combo.
    negative_flex_combo = Beam.check_combo(nested_neg_combo_list)

    # Take the required top flexural reinforcement and put it in a nested list.
    # Index 0 is left, Index 1 is middle, and Index 2 is right.
    top_flex_reinf_needed = initial_flexural_df["Unnamed: 7"].tolist()
    top_flex_reinf_needed = [
        top_flex_reinf_needed[i : i + 3]
        for i in range(0, len(top_flex_reinf_needed), 3)
    ]
    # Check if any of the beams are overstressed. If they are, the values get replaced with O/S.
    top_flex_reinf_needed = [
        [
            "O/S" if str(element).strip().lower() in ["o/s", "nan"] else element
            for element in sublist
        ]
        for sublist in top_flex_reinf_needed
    ]

    # Repeat the same as above but for required bottom flexural reinforcement.
    bot_flex_reinf_needed = initial_flexural_df["Unnamed: 10"].tolist()
    bot_flex_reinf_needed = [
        bot_flex_reinf_needed[i : i + 3]
        for i in range(0, len(bot_flex_reinf_needed), 3)
    ]
    bot_flex_reinf_needed = [
        [
            "O/S" if str(element).strip().lower() in ["o/s", "nan"] else element
            for element in sublist
        ]
        for sublist in bot_flex_reinf_needed
    ]

    # Take the required flexural torsion reinforcement and put it in a nested list.
    # Index 0 is left, Index 1 is middle, and Index 2 is right.
    flex_torsion_reinf_needed = initial_shear_df["Unnamed: 13"].tolist()
    flex_torsion_reinf_needed = [
        flex_torsion_reinf_needed[i : i + 3]
        for i in range(0, len(flex_torsion_reinf_needed), 3)
    ]

    # Check if any of the beams are overstressed in torsion. If they are, values get replaced with O/S.
    flex_torsion_reinf_needed = [
        [
            "O/S" if str(element).strip().lower() in ["o/s", "nan"] else element
            for element in sublist
        ]
        for sublist in flex_torsion_reinf_needed
    ]

    # Take each beam's shear combo and put it in a nested list.
    shear_combo_list = initial_shear_df["Unnamed: 6"].tolist()
    nested_shear_combo = [
        shear_combo_list[i : i + 3] for i in range(0, len(shear_combo_list), 3)
    ]

    # Take the nested list and return OK or OS as a string in a list.
    nested_shear_combo = [
        "O/S"
        if any(str(element).strip().lower() in ["o/s", "nan"] for element in sublist)
        else "OK"
        for sublist in nested_shear_combo
    ]

    # Apply the Beam class method to retrieve whether it is overstressed in shear.
    shear_combo_check = Beam.check_combo(nested_shear_combo)

    # Repeat the same as shear combo, except for torsion combo.
    torsion_combo_list = initial_shear_df["Unnamed: 12"].tolist()
    nested_torsion_combo = [
        torsion_combo_list[i : i + 3] for i in range(0, len(torsion_combo_list), 3)
    ]

    nested_torsion_combo = [
        "O/S"
        if any(str(element).strip().lower() in ["o/s", "nan"] for element in sublist)
        else "OK"
        for sublist in nested_torsion_combo
    ]

    torsion_combo_check = Beam.check_combo(nested_torsion_combo)

    # Take the required shear reinforcement and put it in a nested list.
    # Index 0 is left, Index 1 is middle, and Index 2 is right.
    shear_reinf_needed = initial_shear_df["Unnamed: 7"].tolist()
    shear_reinf_needed = [
        shear_reinf_needed[i : i + 3] for i in range(0, len(shear_reinf_needed), 3)
    ]

    # Check if any of the beams are overstressed in shear. If they are, values get replaced with O/S.
    shear_reinf_needed = [
        [
            "O/S" if str(element).strip().lower() in ["o/s", "nan"] else element
            for element in sublist
        ]
        for sublist in shear_reinf_needed
    ]

    # Repeat the same as required shear reinforcement but for required torsion reinforcement.
    torsion_reinf_needed = initial_shear_df["Unnamed: 10"].tolist()
    torsion_reinf_needed = [
        torsion_reinf_needed[i : i + 3] for i in range(0, len(torsion_reinf_needed), 3)
    ]
    torsion_reinf_needed = [
        [
            "O/S" if str(element).strip().lower() in ["o/s", "nan"] else element
            for element in sublist
        ]
        for sublist in torsion_reinf_needed
    ]

    # Call create_instance function and create instances of all etabs ids.
    beam_instances = [
        create_instance(
            initial_flexural_df,
            e_id,
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
        )
        for e_id, width, depth, pos_flex_combo, neg_flex_combo, req_top_flex_reinf, req_bot_flex_reinf, req_flex_torsion_reinf, shear_combo, torsion_combo, req_shear_reinf, req_torsion_reinf in zip(
            e_ids,
            beam_widths,
            beam_depths,
            positive_flex_combo,
            negative_flex_combo,
            top_flex_reinf_needed,
            bot_flex_reinf_needed,
            flex_torsion_reinf_needed,
            shear_combo_check,
            torsion_combo_check,
            shear_reinf_needed,
            torsion_reinf_needed,
        )
    ]

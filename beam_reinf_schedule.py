import tkinter as tk
import os
from tkinter.filedialog import askopenfilename, asksaveasfilename
import pathlib
import pandas as pd
import Design_Functions.rebar_information as rebar_func
import importlib
import numpy as np
from PIL import Image, ImageTk
import sys


importlib.reload(rebar_func)


def import_file():
    root = tk.Tk()
    root.withdraw()
    filepath = askopenfilename()
    root.destroy()
    return filepath


excel_file = import_file()
initial_df = pd.read_excel(excel_file, sheet_name=None)
pd.set_option("display.max_rows", None)

v1_flexural_df = initial_df["Conc Bm Flx Env - ACI 318-19"].drop([0, 1])
v1_shear_df = initial_df["Conc Bm Shr Env - ACI 318-19"].drop([0, 1])
v1_flexural_df.reset_index(drop=True, inplace=True)
v1_shear_df.reset_index(drop=True, inplace=True)

v2_flexural_df = v1_flexural_df.drop(
    ["Unnamed: 2", "Unnamed: 5", "Unnamed: 6", "Unnamed: 8", "Unnamed: 9"], axis=1
).copy()
v2_shear_df = v1_shear_df.drop(
    [
        "Unnamed: 1",
        "Unnamed: 2",
        "Unnamed: 3",
        "Unnamed: 4",
        "Unnamed: 5",
        "Unnamed: 6",
        "Unnamed: 8",
        "Unnamed: 9",
        "Unnamed: 11",
        "Unnamed: 12",
    ],
    axis=1,
).copy()

v3_flexural_df = v2_flexural_df.iloc[::3].copy()

v2_flexural_df.reset_index(drop=True, inplace=True)

v3_flexural_df.insert(3, "Width (mm)", None)
v3_flexural_df.insert(4, "Depth (mm)", None)

v3_flexural_df.loc[:, "Width (mm)"] = v3_flexural_df["Unnamed: 3"].apply(
    rebar_func.clean_width_dimensions
)

v3_flexural_df.loc[:, "Depth (mm)"] = v3_flexural_df["Unnamed: 3"].apply(
    rebar_func.clean_depth_dimensions
)

v4_flexural_df = v3_flexural_df.drop(
    ["Unnamed: 3", "Unnamed: 4", "Unnamed: 7", "Unnamed: 10"], axis=1
).copy()

v4_flexural_df = v4_flexural_df.rename(columns={"Unnamed: 1": "ETABS beam ID"})
v2_shear_df = v2_shear_df.rename(
    columns={
        "Unnamed: 7": "Shear rebar area (mm2/m)",
        "Unnamed: 10": "Shear Torsion rebar area (mm2/m)",
        "Unnamed: 13": "Torsional Rebar (mm2)",
    }
)

# Create dataframe which reflects column headings
columns = pd.MultiIndex.from_tuples(
    [
        ("Storey", ""),
        ("Etabs ID", ""),
        ("Dimensions", "Width (mm)"),
        ("Dimensions", "Depth (mm)"),
        ("Bottom Reinforcement", "Left (BL)"),
        ("Bottom Reinforcement", "Middle (B)"),
        ("Bottom Reinforcement", "Right (BR)"),
        ("Top Reinforcement", "Left (TL)"),
        ("Top Reinforcement", "Middle (T)"),
        ("Top Reinforcement", "Right (TR)"),
        ("Side Face Reinforcement", "Left"),
        ("Side Face Reinforcement", ""),
        ("Side Face Reinforcement", "Right"),
        ("Shear links", "Left (H)"),
        ("Shear links", "Middle (J)"),
        ("Shear links", "Right (K)"),
    ]
)
beam_schedule_df = pd.DataFrame(columns=columns)

beam_schedule_df["Storey"] = v4_flexural_df[
    "TABLE:  Concrete Beam Flexure Envelope - ACI 318-19"
]
beam_schedule_df["Etabs ID"] = v4_flexural_df["ETABS beam ID"]
beam_schedule_df["Dimensions", "Width (mm)"] = v4_flexural_df["Width (mm)"]
beam_schedule_df["Dimensions", "Depth (mm)"] = v4_flexural_df["Depth (mm)"]
beam_schedule_df.reset_index(drop=True, inplace=True)

v2_shear_df.reset_index(drop=True, inplace=True)
v5_flexural_df = v2_flexural_df.drop(
    ["TABLE:  Concrete Beam Flexure Envelope - ACI 318-19", "Unnamed: 1", "Unnamed: 3"],
    axis=1,
).copy()
v5_flexural_df = v5_flexural_df.rename(
    columns={
        "Unnamed: 4": "Location",
        "Unnamed: 10": "Bottom reinforcement",
        "Unnamed: 7": "Top Reinforcement",
    }
)
v5_flexural_df.reset_index(drop=True, inplace=True)
v5_flexural_df["Torsional Rebar (mm2)"] = v2_shear_df["Torsional Rebar (mm2)"]

# create new columns
v5_flexural_df["Width (mm)"] = [1] * len(v5_flexural_df)
v5_flexural_df["Depth (mm)"] = [1] * len(v5_flexural_df)
v5_flexural_df["ETABS beam ID"] = [1] * len(v5_flexural_df)
# add new columns to beginning of dataframe, create v6
cols = ["ETABS beam ID", "Width (mm)", "Depth (mm)"] + [
    c
    for c in v5_flexural_df.columns
    if c not in ["ETABS beam ID", "Width (mm)", "Depth (mm)"]
]
v6_flexural_df = v5_flexural_df[cols].copy()

v6_flexural_df.loc[:, "Width (mm)"] = v2_flexural_df["Unnamed: 3"].apply(
    rebar_func.clean_width_dimensions
)
v6_flexural_df.loc[:, "Depth (mm)"] = v2_flexural_df["Unnamed: 3"].apply(
    rebar_func.clean_depth_dimensions
)
v6_flexural_df.insert(4, "Flexural overstressed (Combo 1)", "-")
v6_flexural_df.insert(5, "Flexural overstressed (Combo 2)", "-")
v6_flexural_df.insert(6, "Shear overstressed", "-")
v6_flexural_df.loc[:, "Shear overstressed"] = v1_shear_df.apply(
    rebar_func.shear_overstressed_check, axis=1, args=["Unnamed: 6"]
)
v6_flexural_df.loc[:, "Flexural overstressed (Combo 1)"] = v1_flexural_df.apply(
    rebar_func.flex_overstressed_check, axis=1, args=("Unnamed: 6", "Unnamed: 9")
)  # check if beam is overstressed in flexure
v6_flexural_df.loc[:, "Flexural overstressed (Combo 2)"] = v1_flexural_df.apply(
    rebar_func.flex_overstressed_check, axis=1, args=("Unnamed: 6", "Unnamed: 9")
)  # check if beam is overstressed in flexure
v6_flexural_df.loc[:, "ETABS beam ID"] = v2_flexural_df["Unnamed: 1"]
v6_flexural_df.insert(8, "Residual Rebar (mm2)", "-")

# v6_flexural_df.loc[:, 'Bottom reinforcement', 'Top Reinforcement'] = rebar_func.side_face_assessment(
#     v6_flexural_df,
#     "Depth (mm)",
#     "Torsional Rebar (mm2)",
#     "Bottom reinforcement",
#     "Top Reinforcement",
# )

v6_flexural_df = rebar_func.add_long_rebar(v6_flexural_df, 'Depth (mm)', 'Torsional Rebar (mm2)', 'Bottom reinforcement', 'Top Reinforcement')

# v6_flexural_df.loc[:, 'Bottom Reinforcement'] = rebar_func.side_face_assessment(
#     v6_flexural_df,
#     "Depth (mm)",
#     "Torsional Rebar (mm2)",
#     "Bottom reinforcement",
#     "Top Reinforcement",
# )

v6_flexural_df.loc[:, "Rebar Count"] = v6_flexural_df.loc[:, "Width (mm)"].apply(
    rebar_func.rebar_count
)
v6_flexural_df.loc[:, "Bottom Rebar Schedule"] = v6_flexural_df.apply(
    rebar_func.rebar_string,
    axis=1,
    args=(
        "Rebar Count",
        "Bottom reinforcement",
        # "Flexural overstressed (Combo 1)",
        "Flexural overstressed (Combo 2)",
    ),
)
v6_flexural_df.loc[:, "Top Rebar Schedule"] = v6_flexural_df.apply(
    rebar_func.rebar_string,
    axis=1,
    args=(
        "Rebar Count",
        "Top Reinforcement",
        "Flexural overstressed (Combo 1)",
        # "Flexural overstressed (Combo 2)",
    ),
)
v6_flexural_df.insert(
    9,
    "Bottom Rebar Area Provided (mm2)",
    v6_flexural_df.apply(
        rebar_func.rebar_area,
        axis=1,
        args=(
            "Rebar Count",
            "Bottom reinforcement",
            # "Flexural overstressed (Combo 1)",
            "Flexural overstressed (Combo 2)",
        ),
    ),
)
v6_flexural_df.insert(
    11,
    "Top Rebar Area Provided (mm2)",
    v6_flexural_df.apply(
        rebar_func.rebar_area,
        axis=1,
        args=(
            "Rebar Count",
            "Top Reinforcement",
            "Flexural overstressed (Combo 1)",
            # "Flexural overstressed (Combo 2)",
        ),
    ),
)
v6_flexural_df.loc[:, "Residual Rebar (mm2)"] = v6_flexural_df.apply(
    lambda row: rebar_func.residual_rebar(
        row,
        "Bottom Rebar Area Provided (mm2)",
        "Bottom reinforcement",
        "Top Rebar Area Provided (mm2)",
        "Top Reinforcement",
    ),
    axis=1,
)
v6_flexural_df.loc[:, "Side Face Clear Space (mm)"] = v6_flexural_df[
    "Depth (mm)"
].apply(rebar_func.side_face_count)

v6_flexural_df.insert(14, "Side Face Reinforcement Provided (mm2)", "-")
v6_flexural_df.loc[:, "Side Face Reinforcement Provided (mm2)"] = v6_flexural_df.apply(
    rebar_func.side_face_area,
    axis=1,
    args=(
        "Torsional Rebar (mm2)",
        "Side Face Clear Space (mm)",
        "Residual Rebar (mm2)",
        "Shear overstressed",
    ),
)
v6_flexural_df.loc[:, "Side Face Reinforcement Schedule"] = v6_flexural_df.apply(
    rebar_func.side_face_reinf,
    axis=1,
    args=(
        "Torsional Rebar (mm2)",
        "Side Face Clear Space (mm)",
        "Residual Rebar (mm2)",
        "Shear overstressed",
    ),
)
move_1, move_2, move_3, move_4 = (
    v6_flexural_df.pop("Residual Rebar (mm2)"),
    v6_flexural_df.pop("Top Rebar Area Provided (mm2)"),
    v6_flexural_df.pop("Bottom Rebar Area Provided (mm2)"),
    v6_flexural_df.pop("Side Face Clear Space (mm)"),
)
v6_flexural_df.insert(8, "Top Rebar Area Provided (mm2)", move_2)
v6_flexural_df.insert(10, "Bottom Rebar Area Provided (mm2)", move_3)
v6_flexural_df.insert(11, "Residual Rebar (mm2)", move_1)
v6_flexural_df.insert(14, "Side Face Clear Space (mm)", move_4)

# begin calculation process for shear reinforcement
v2_shear_df.loc[:, "Shear rebar area (mm2/m)"] = v2_shear_df[
    "Shear rebar area (mm2/m)"
].fillna("O/S")
v2_shear_df.loc[:, "Required Shear Area (mm2)"] = v2_shear_df.apply(
    rebar_func.shear_area_req,
    axis=1,
    args=("Shear rebar area (mm2/m)", "Shear Torsion rebar area (mm2/m)"),
)
v2_shear_df.insert(1, "Width (mm)", v6_flexural_df["Width (mm)"])
v2_shear_df.insert(6, "Required Shear Legs", "-")
v2_shear_df.loc[:, "Required Shear Legs"] = v2_shear_df["Width (mm)"].apply(
    rebar_func.req_legs
)
v2_shear_df.insert(7, "Shear Link Schedule", "-")
v2_shear_df.loc[:, "Shear Link Schedule"] = v2_shear_df.apply(
    rebar_func.shear_string,
    axis=1,
    args=(
        "Required Shear Legs",
        "Required Shear Area (mm2)",
        "Shear rebar area (mm2/m)",
    ),
)
v2_shear_df.insert(7, "Shear area provided (mm2)", "-")
v2_shear_df.loc[:, "Shear area provided (mm2)"] = v2_shear_df.apply(
    rebar_func.shear_area,
    axis=1,
    args=(
        "Required Shear Legs",
        "Required Shear Area (mm2)",
        "Shear rebar area (mm2/m)",
    ),
)

# from v6 create v7
# only includes bottom, top, and side face sched
v7_flexural_df = v6_flexural_df.drop(
    [
        "Width (mm)",
        "Depth (mm)",
        "Location",
        "Bottom reinforcement",
        "Top Reinforcement",
        "Torsional Rebar (mm2)",
        "Rebar Count",
        "Side Face Clear Space (mm)",
        "Residual Rebar (mm2)",
        "Bottom Rebar Area Provided (mm2)",
        "Top Rebar Area Provided (mm2)",
    ],
    axis=1,
).copy()
v7_flexural_df.reset_index(drop=True, inplace=True)
v3_shear_df = v2_shear_df.drop(
    [
        "Width (mm)",
        "Shear rebar area (mm2/m)",
        "Shear Torsion rebar area (mm2/m)",
        "Torsional Rebar (mm2)",
        "Required Shear Area (mm2)",
        "Required Shear Legs",
    ],
    axis=1,
).copy()
v3_shear_df = v3_shear_df.iloc[:, 1:].copy()
v3_shear_df.reset_index(drop=True, inplace=True)

side_face_df = v7_flexural_df.drop(
    [
        "ETABS beam ID",
        "Flexural overstressed (Combo 1)",
        "Flexural overstressed (Combo 2)",
        "Shear overstressed",
        "Top Rebar Schedule",
        "Bottom Rebar Schedule",
    ],
    axis=1,
).copy()


# take the maximum side face reinforcement schedule
def replace_with_max(group):
    # Convert 'Side Face Reinforcement Provided (mm2)' to numeric, making non-numeric values NaN
    group["Side Face Reinforcement Provided (mm2)"] = pd.to_numeric(
        group["Side Face Reinforcement Provided (mm2)"], errors="coerce"
    )

    # If all values are NaN, leave the group as it is
    if group["Side Face Reinforcement Provided (mm2)"].isna().all():
        return group

    # Find the row with the maximum value
    max_row = group.loc[group["Side Face Reinforcement Provided (mm2)"].idxmax()]

    # Replace all values in the group with the values from the max row
    group["Side Face Reinforcement Provided (mm2)"] = max_row[
        "Side Face Reinforcement Provided (mm2)"
    ]
    group["Side Face Reinforcement Schedule"] = max_row[
        "Side Face Reinforcement Schedule"
    ]
    return group


# Create a 'Group' column for grouping
side_face_df["Group"] = np.repeat(range(len(side_face_df) // 3), 3)

# Apply the function to each group
side_face_df = side_face_df.groupby("Group").apply(replace_with_max)

# Drop the 'Group' column
side_face_df = side_face_df.drop(columns="Group")

side_face_df = side_face_df.reset_index(drop=True)

# update v7_flexural_df with new side face reinf schedule

side_face_df = side_face_df.drop(columns="Side Face Reinforcement Provided (mm2)")

v7_flexural_df["Side Face Reinforcement Schedule"] = side_face_df[
    "Side Face Reinforcement Schedule"
]


# take the maximum shear link schedule for all sides of beam
def replace_with_max_shear(group):
    # Convert 'Shear area provided (mm2)' to numeric, making non-numeric values NaN
    group["Shear area provided (mm2)"] = pd.to_numeric(
        group["Shear area provided (mm2)"], errors="coerce"
    )

    # If all values are NaN, leave the group as it is
    if group["Shear area provided (mm2)"].isna().all():
        return group
    # If any value is NaN, replace all values with 'Over-stressed. Please reassess'
    elif group["Shear area provided (mm2)"].isna().any():
        group["Shear area provided (mm2)"] = "Overstressed. Please reassess"
        group["Shear Link Schedule"] = "Overstressed. Please reassess"
        return group
    else:
        # Find max value
        max_row = group.loc[group["Shear area provided (mm2)"].idxmax()]

        # replace all values in the group with the values from the max row
        group["Shear area provided (mm2)"] = max_row["Shear area provided (mm2)"]
        group["Shear Link Schedule"] = max_row["Shear Link Schedule"]
        return group


# Create a 'Group' column for grouping
v3_shear_df["Group"] = np.repeat(range(len(v3_shear_df) // 3), 3)

# Apply the function to each group
v3_shear_df = v3_shear_df.groupby("Group").apply(replace_with_max_shear)

# Drop the 'Group' column
v3_shear_df = v3_shear_df.drop(columns="Group")

v3_shear_df = v3_shear_df.reset_index(drop=True)

# update v7_flexural_df with new side face reinf schedule

v3_shear_df = v3_shear_df.drop(columns="Shear area provided (mm2)")


v3_shear_df["new_index"] = np.repeat(range(len(v3_shear_df) // 3), 3)[
    : len(v3_shear_df)
]
v3_shear_df_grouped = (
    v3_shear_df.groupby("new_index")["Shear Link Schedule"]
    .apply(list)
    .apply(pd.Series)
    .reset_index(drop=True)
)

v7_flexural_df["new_index"] = np.repeat(range(len(v7_flexural_df) // 3), 3)[
    : len(v7_flexural_df)
]
v7_flexural_df_grouped_Bottom_Rebar = (
    v7_flexural_df.groupby("new_index")["Bottom Rebar Schedule"]
    .apply(list)
    .apply(pd.Series)
    .reset_index(drop=True)
    .copy()
)
v7_flexural_df_grouped_Top_Rebar = (
    v7_flexural_df.groupby("new_index")["Top Rebar Schedule"]
    .apply(list)
    .apply(pd.Series)
    .reset_index(drop=True)
    .copy()
)
v7_flexural_df_grouped_Side_Rebar = (
    v7_flexural_df.groupby("new_index")["Side Face Reinforcement Schedule"]
    .apply(list)
    .apply(pd.Series)
    .reset_index(drop=True)
    .copy()
)

beam_schedule_df[("Bottom Reinforcement", "Left (BL)")].update(
    v7_flexural_df_grouped_Bottom_Rebar[0]
)
beam_schedule_df[("Bottom Reinforcement", "Middle (B)")].update(
    v7_flexural_df_grouped_Bottom_Rebar[1]
)
beam_schedule_df[("Bottom Reinforcement", "Right (BR)")].update(
    v7_flexural_df_grouped_Bottom_Rebar[2]
)
beam_schedule_df[("Top Reinforcement", "Left (TL)")].update(
    v7_flexural_df_grouped_Top_Rebar[0]
)
beam_schedule_df[("Top Reinforcement", "Middle (T)")].update(
    v7_flexural_df_grouped_Top_Rebar[1]
)
beam_schedule_df[("Top Reinforcement", "Right (TR)")].update(
    v7_flexural_df_grouped_Top_Rebar[2]
)
beam_schedule_df[("Side Face Reinforcement", "Left")].update(
    v7_flexural_df_grouped_Side_Rebar[0]
)
beam_schedule_df[("Side Face Reinforcement", "")].update(
    v7_flexural_df_grouped_Side_Rebar[1]
)
beam_schedule_df[("Side Face Reinforcement", "Right")].update(
    v7_flexural_df_grouped_Side_Rebar[2]
)
beam_schedule_df[("Shear links", "Left (H)")].update(v3_shear_df_grouped[0])
beam_schedule_df[("Shear links", "Middle (J)")].update(v3_shear_df_grouped[1])
beam_schedule_df[("Shear links", "Right (K)")].update(v3_shear_df_grouped[2])

# drop the left and right subcolumns of side face reinforcement in beam_schedule_df
beam_schedule_final_df = beam_schedule_df.copy()
beam_schedule_final_df = beam_schedule_final_df.drop(
    [("Side Face Reinforcement", "Left"), ("Side Face Reinforcement", "Right")], axis=1
)

beam_schedule_final_df.columns = beam_schedule_final_df.columns.set_levels(
    [level.str.strip() for level in beam_schedule_final_df.columns.levels], level=[0, 1]
)
beam_schedule_final_df.apply(
    rebar_func.quick_side_check,
    args=(
        ("Dimensions", "Depth (mm)"),
        ("Side Face Reinforcement", ""),
    ),
    axis=1,
)


def export_file(beam_schedule_df):
    root = tk.Tk()
    root.withdraw()
    filepath = asksaveasfilename(defaultextension=".xlsx")
    root.destroy()
    if filepath:
        beam_schedule_final_df.to_excel(filepath, index=True)
        sys.exit()


def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


# create main program
gui = tk.Tk()

# create window geometry and title
gui.geometry("900x350")
gui.title("Beam Reinforcement Scheduling Program - Made by Adnan @ KLD")

# Create title inside program
main_title = tk.Label(
    gui,
    text="Beam Reinforcement Scheduling Program. Made by Adnan @ KLD",
    font=("Helvetica", 18),
)
main_title.pack(padx=50, pady=20)

# Put KLD design logo
image_path = resource_path(
    "killa-design.jpg"
)  # use the resource_path function to get the correct path
kld_logo = Image.open(image_path)  # Then use this path to open the image
photo = ImageTk.PhotoImage(kld_logo)
label = tk.Label(gui, image=photo)
label.pack(side="top", fill="both", padx=50)

# Put the button to ask for the name of the completed excel file and to download it

final_button = tk.Button(
    gui,
    text="Please download Completed Beam Reinforcement Schedule",
    font=("Helvetica", 15),
    command=lambda: export_file(beam_schedule_df),
)
final_button.pack(padx=50, pady=10)


gui.mainloop()

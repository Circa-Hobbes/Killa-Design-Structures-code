from beam_calculator_class import Beam
import pandas as pd
import os
from PIL import Image, ImageTk
import tkinter as tk
import sys
from tkinter.filedialog import askopenfilename, asksaveasfilename


# Create all instances of Beam class.
def create_instance(
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
    torsion_combo_list = initial_shear_df["Unnamed: 9"].tolist()
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

    # Call create_instance function and create instances of all beams.
    beam_instances = [
        create_instance(
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

    # Begin with for loop and create attributes for each beam instance to undertake calculations.
    for beam in beam_instances:
        # Get the effective depth by multiplying the depth by 0.8.
        beam.get_eff_depth()
        # Get the longitudinal rebar count.
        beam.get_long_count()

        # Split the torsion reinforcement to the top and bottom rebar if the depth <= 600mm.
        beam.flex_torsion_splitting()

        # Begin calculating the required top and bottom longitudinal reinforcement.
        beam.get_top_flex_rebar_string()
        beam.get_top_flex_rebar_area()

        beam.get_bot_flex_rebar_string()
        beam.get_bot_flex_rebar_area()

        # Calculate the residual rebar obtained from the provided against the required.
        beam.get_residual_rebar()

        # Calculate the required shear legs based on the beams width.
        beam.get_shear_legs()

        # Calculate the total required shear reinforcement including shear and torsion.
        beam.get_total_shear_req()

        # Calculate the provided shear reinforcement string and area.
        beam.get_shear_string()
        beam.get_shear_area()

        # Check and replace if necessary the maximum longitudinal shear spacing against Clause 18.4.2.4 of ACI 318-19.
        beam.get_min_shear_long_spacing()
        beam.modify_shear_reinf()

        # Grab the index of the shear reinforcement with the highest area.
        # beam.get_index_for_shear_reinf()

        # Calculate the allowable side face clear space in beams which have a depth greater than 600mm.
        beam.get_side_face_clear_space()

        # Calculate the provided side face reinforcement string and area.
        beam.get_side_face_string()
        beam.get_side_face_area()

        # Grab the index of the side face reinforcement with the highest area.
        beam.get_index_for_side_face_reinf()

# Create dataframe to fill data with.
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
        ("Side Face Reinforcement", ""),
        ("Shear links", "Left (H)"),
        ("Shear links", "Middle (J)"),
        ("Shear links", "Right (K)"),
    ]
)
beam_schedule_df = pd.DataFrame(columns=columns)

# Apply the storey data to the storey column in the beam schedule dataframe.
beam_schedule_df.loc[:, "Storey"] = initial_flexural_df[
    "TABLE:  Concrete Beam Flexure Envelope - ACI 318-19"
].iloc[::3]

# Map the relevant beam attributes to the beam schedule dataframe columns:
beam_mapping = {
    "id": ("Etabs ID", ""),
    "width": ("Dimensions", "Width (mm)"),
    "depth": ("Dimensions", "Depth (mm)"),
    "flex_bot_left_rebar_string": ("Bottom Reinforcement", "Left (BL)"),
    "flex_bot_middle_rebar_string": ("Bottom Reinforcement", "Middle (B)"),
    "flex_bot_right_rebar_string": ("Bottom Reinforcement", "Right (BR)"),
    "flex_top_left_rebar_string": ("Top Reinforcement", "Left (TL)"),
    "flex_top_middle_rebar_string": ("Top Reinforcement", "Middle (T)"),
    "flex_top_right_rebar_string": ("Top Reinforcement", "Right (TR)"),
    "selected_side_face_reinforcement_string": ("Side Face Reinforcement", ""),
    "shear_left_string": ("Shear links", "Left (H)"),
    "shear_middle_string": ("Shear links", "Middle (J)"),
    "shear_right_string": ("Shear links", "Right (K)"),
}

# Loop through all the beam instances and populate the beam schedule dataframe with relevant information.
for idx, beam in enumerate(beam_instances):  # type: ignore
    for attr, col in beam_mapping.items():
        beam_schedule_df.loc[idx, col] = getattr(beam, attr)


# Create the relevant functions to export the excel file
def export_file(beam_schedule_df):
    # Ask the user for the file path to save the Excel file
    filepath = asksaveasfilename(defaultextension=".xlsx")

    # Create an Excel writer object
    writer = pd.ExcelWriter(filepath, engine="xlsxwriter")

    # Write the entire DataFrame to the first sheet
    beam_schedule_df.to_excel(writer, sheet_name="Beam Reinforcement Schedule")

    # Group by the 'Storey' column
    grouped = beam_schedule_df.groupby("Storey")

    # Iterate through the groups and write to separate sheets
    for name, group in grouped:
        sheet_name = f"Storey {name}"
        group.to_excel(writer, sheet_name=sheet_name)

    # Save the Excel file
    writer.close()
    sys.exit()


def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS  # type: ignore
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
    text="Please Download the Completed Beam Reinforcement Schedule",
    font=("Helvetica", 15),
    command=lambda: export_file(beam_schedule_df),
)
final_button.pack(padx=50, pady=10)

# Run the main loop to execute the program.
gui.mainloop()

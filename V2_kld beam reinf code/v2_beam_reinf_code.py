# import Design_Functions.rebar_information as rebar_func
from beam_calculator_class import Beam
import pandas as pd

# import importlib
import numpy as np
import tkinter as tk

# import sys
import importlib
from tkinter.filedialog import askopenfilename, asksaveasfilename

# importlib.reload(rebar_func)


# Create an instance of the Beam class for when the script is run, not when the module
# is imported.
def create_instance():
    beam = Beam()
    return beam


if __name__ == "__main__":
    instance = create_instance()


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

# Slice through flexural dataframe to obtain all the ETAB beam IDs.
flexural = Beam(initial_flexural_df)
e_id = flexural.obtain_id()

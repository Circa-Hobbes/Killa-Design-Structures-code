# import Design_Functions.rebar_information as rebar_func
# import design_classes.beam_calculator_class as beam
import pandas as pd
import importlib
import numpy as np
import tkinter as tk
import sys
import importlib
from tkinter.filedialog import askopenfilename, asksaveasfilename

# importlib.reload(rebar_func)
# importlib.reload(beam)


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

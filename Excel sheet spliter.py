import tkinter as tk
import os
from tkinter.filedialog import askopenfilename, asksaveasfilename
import pathlib
import pandas as pd
import importlib
import numpy as np
from PIL import Image, ImageTk
import sys


def import_file():
    root = tk.Tk()
    root.withdraw()
    filepath = askopenfilename()
    root.destroy()
    return filepath


excel_file = import_file()
df = pd.read_excel(excel_file, sheet_name=None)
pd.set_option("display.max_rows", None)

# Get unique categories
categories = df["Sheet1"]["Storey"].unique()

writer = pd.ExcelWriter("output.xlsx", engine="xlsxwriter")

for sheet_name, sheet_df in df.items():
    if "Storey" in sheet_df.columns:
        categories = sheet_df["Storey"].unique()
        for category in categories:
            df_category = sheet_df[sheet_df["Storey"] == category]
            df_category.to_excel(
                writer, sheet_name=f"{sheet_name}_{category}", index=False
            )
writer.close()

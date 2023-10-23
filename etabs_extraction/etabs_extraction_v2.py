import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from openpyxl import Workbook
from openpyxl.utils import get_column_letter
from openpyxl.drawing.image import Image
import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
from PIL import Image, ImageTk
from Extraction import Extraction as ex

if __name__ == "__main__":
    SapModel = ex.initialise_sap_model()
    if SapModel != None:
        if ex.is_locked(SapModel) == False:
            print(
                "ETABS instance identified, but model is not locked. Please run model and try again!"
            )  # This will need to be updated later on in the code for the GUI.
        else:
            ex.clear_combos(SapModel)

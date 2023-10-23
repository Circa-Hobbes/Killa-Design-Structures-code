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
    SapModel = ex.initialise_sap_model()[0]
    if SapModel == None:
        assess_instance = (
            "No running instance of the program found or failed to attach."
        )
    else:
        ex.is_locked(SapModel)

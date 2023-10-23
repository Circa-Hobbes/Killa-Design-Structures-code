import numpy as np
import pandas as pd
import sys
import comtypes.client


class Extraction:
    """This class aims to provide functionality to enable the extraction, plotting, and calculation of ETABS structural metrics."""

    def __init__(
        self,
        overall_wind_displacement_combolist,
        wind_interstory_drift_combolist,
        seismic_interstory_drift_combolist,
        story_shear_combolist,
        overall_building_weight_combolist,
        nonscaled_base_shear_combolist,
        scaled_base_shear_combolist,
        time_period_combolist,
    ):
        self.combolists = {
            """This dictionary contains the attributes of all the extracted combo lists.
        """
            "overall_wind_displacement": overall_wind_displacement_combolist,
            "wind_interstory_drift": wind_interstory_drift_combolist,
            "seismic_interstory_drift": seismic_interstory_drift_combolist,
            "story_shear": story_shear_combolist,
            "overall_building_weight": overall_building_weight_combolist,
            "nonscaled_base_shear": nonscaled_base_shear_combolist,
            "scaled_base_shear": scaled_base_shear_combolist,
            "time_period": time_period_combolist,
        }

    @staticmethod
    def initialise_sap_model():
        # Create API helper object.
        helper = comtypes.client.CreateObject("ETABSv1.Helper")
        helper = helper.QueryInterface(comtypes.gen.ETABSv1.cHelper)  # type: ignore
        assess_instance = ""
        SapModel = None

        try:
            # Get the current ETABS instance.
            myETABSObject = helper.GetObject("CSI.ETABS.API.ETABSObject")
        except (OSError, comtypes.COMError):
            assess_instance = (
                "No running instance of the program found or failed to attach."
            )
            sys.exit(-1)

        # Create SapModel object (ETABS instance)
        try:
            SapModel = myETABSObject.SapModel
        except AttributeError:
            assess_instance = (
                "No running instance of the program found or failed to attach."
            )

        return SapModel, assess_instance

    @staticmethod
    def is_locked(SapModel: object) -> bool:
        """This static method checks if the SapModel is locked or not.

        Args:
            SapModel (object): The ETABS object.

        Returns:
            bool: True if it is locked, False if it's not locked.
        """
        if SapModel.GetModelIsLocked():  # type: ignore
            return True
        else:
            return False

    @staticmethod
    def clear_combos(SapModel: object):
        SapModel.DatabaseTables.SetLoadCombinationsSelectedForDisplay([""])  # type: ignore
        SapModel.DatabaseTables.SetLoadCasesSelectedForDisplay([""])  # type: ignore
        SapModel.DatabaseTables.SetLoadPatternsSelectedForDisplay([""])  # type: ignore

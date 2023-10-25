# import numpy as np
# import pandas as pd
# import comtypes.client
# import matplotlib.pyplot as plt
# import sys


# class Extraction:
#     """This class aims to provide functionality to enable the extraction, plotting, and calculation of ETABS structural metrics."""

#     def __init__(
#         self,
#         combo_list,
#     ):
#         self.combo_list = combo_list
#         self.filtered_combo_list = None
#         self.extracts = {
#             "story_heights": pd.DataFrame(),
#         }
#         self.tables = {
#             "overall_wind_displacement_max": [],
#             "overall_wind_displacement_min": [],
#         }

#     @staticmethod
#     def initialise_sap_model() -> object:
#         """This static method initialises the ETABS SapModel for other methods to utilise.

#         Returns:
#             object: The ETABS SapModel object.
#         """
#         # Create API helper object.
#         helper = comtypes.client.CreateObject("ETABSv1.Helper")
#         helper = helper.QueryInterface(comtypes.gen.ETABSv1.cHelper)  # type: ignore

#         try:
#             # Get the current ETABS instance.
#             myETABSObject = helper.GetObject("CSI.ETABS.API.ETABSObject")
#         except (OSError, comtypes.COMError):
#             SapModel = None
#             sys.exit(-1)

#         # Create SapModel object (ETABS instance)
#         try:
#             SapModel = myETABSObject.SapModel
#         except AttributeError:
#             SapModel = None
#             print("No running instance of the program found or failed to attach.")

#         return SapModel

#     @staticmethod
#     def exit_sap_model(SapModel: object):  # type: ignore
#         SapModel = None
#         return SapModel

#     @staticmethod
#     def is_locked(SapModel: object) -> bool:
#         """This static method checks if the SapModel is locked or not.

#         Args:
#             SapModel (object): The ETABS SapModel object.

#         Returns:
#             bool: True if it is locked, False if it's not locked.
#         """
#         if SapModel.GetModelIsLocked():  # type: ignore
#             return True
#         else:
#             return False

#     @staticmethod
#     def clear_combos(SapModel: object):
#         """This static method clears all the load cases and combinations of the attached SapModel.

#         Args:
#             SapModel (object): The ETABS SapModel object.
#         """
#         SapModel.DatabaseTables.SetLoadCombinationsSelectedForDisplay([""])  # type: ignore
#         SapModel.DatabaseTables.SetLoadCasesSelectedForDisplay([""])  # type: ignore
#         SapModel.DatabaseTables.SetLoadPatternsSelectedForDisplay([""])  # type: ignore

#     def get_story_heights(self, SapModel: object):
#         """This method extracts and formulates a pandas table containing the story height and elevations.
#         Args:
#             SapModel (object): The ETABS SapModel object.
#         """
#         # Grab the story definitions and the tower and base story definitions tables.
#         story_definition_table = SapModel.DatabaseTables.GetTableForDisplayArray("Story Definitions", GroupName="")  # type: ignore
#         baseStory_table = SapModel.DatabaseTables.GetTableForDisplayArray(  # type: ignore
#             "Tower and Base Story Definitions", GroupName=""
#         )
#         # Extract the column headings and number of rows from the tables. This needs to be done as the data is currently an array.
#         cols = story_definition_table[2]
#         num_rows = story_definition_table[3]

#         cols_base = baseStory_table[2]
#         num_rows_base = baseStory_table[3]

#         # Input data into array split.
#         table_data = np.array_split(story_definition_table[4], num_rows)
#         base_data = np.array_split(baseStory_table[4], num_rows_base)

#         # Create story and base definition dataframes.
#         storyDefinitions_df = pd.DataFrame(table_data)
#         storyDefinitions_df.columns = cols

#         baseDefinitions_df = pd.DataFrame(base_data)
#         baseDefinitions_df.columns = cols_base

#         # Delete all columns except story and height.
#         storyDefinitions_df = storyDefinitions_df.drop(
#             ["Tower", "IsMaster", "SimilarTo", "IsSpliced", "Color", "GUID"], axis=1
#         )

#         # Rename height column to Story Height (m)
#         storyDefinitions_df = storyDefinitions_df.rename(
#             columns={"Height": "Story Height (m)"}
#         )

#         # Convert all data in story height column to metre from millimeter.
#         storyDefinitions_df["Story Height (m)"] = storyDefinitions_df[
#             "Story Height (m)"
#         ].astype(float)
#         baseDefinitions_df["BSElev"] = baseDefinitions_df["BSElev"].astype(float)
#         storyDefinitions_df["Story Height (m)"] = (
#             storyDefinitions_df["Story Height (m)"] / 1000
#         )
#         baseDefinitions_df["BSElev"] = baseDefinitions_df["BSElev"] / 1000

#         # Convert the base elevation to an absolute to enable it to be subtracted for more clarity.
#         baseDefinitions_df["BSElev"] = baseDefinitions_df["BSElev"].abs()

#         # Insert Elevation (m) column.
#         storyDefinitions_df.insert(loc=1, column="Elevation (m)", value=0)

#         # Subtract the groundfloor story height by the basement height and add it to GF elevation. The basement height value must be altered manually.
#         storyDefinitions_df.at[storyDefinitions_df.index[-1], "Elevation (m)"] = (
#             storyDefinitions_df.at[storyDefinitions_df.index[-1], "Story Height (m)"]
#             - baseDefinitions_df.loc[0, "BSElev"]
#         )

#         # Loop through the dataframe and sum the story heights to get the total building elevation
#         for i in reversed(range(1, len(storyDefinitions_df))):
#             storyDefinitions_df.loc[i - 1, "Elevation (m)"] = storyDefinitions_df.loc[i, "Elevation (m)"] + storyDefinitions_df.loc[i - 1, "Story Height (m)"]  # type: ignore

#         # Assign storyDefinitions table to attribute
#         self.extracts["story_heights"] = storyDefinitions_df

#     def get_filtered_list(self):
#         """This method grabs the combo_list inputted by the user and filters it so no None values exist."""
#         self.filtered_combo_list = [i for i in self.combo_list if i != None]

#     def calculate_overall_wind_displacement(self, SapModel: object):
#         for combo in self.filtered_combo_list:  # type: ignore
#             # Reset all the load cases and combinations.
#             Extraction.clear_combos(SapModel)

#             # Combo[0] is load combination, combo[1] is load case.
#             if combo[0] == 0:
#                 SapModel.DatabaseTables.SetLoadCombinationsSelectedForDisplay(  # type: ignore
#                     [combo[1]]
#                 )
#                 # Grab the diaphragm center of mass displacements table.
#                 mass_displacement_table = SapModel.DatabaseTables.GetTableForDisplayArray("Diaphragm Center Of Mass Displacements", GroupName="")  # type: ignore

#                 # Extract the column headings and number of rows from the table. This needs to be done as the data is currently an array.
#                 cols = mass_displacement_table[2]
#                 num_rows = mass_displacement_table[3]

#                 # Input data into array split.
#                 table_data = np.array_split(mass_displacement_table[4], num_rows)

#                 # Create wind displacement dataframe.
#                 windDisplacement_df = pd.DataFrame(table_data)
#                 windDisplacement_df.columns = cols

#                 # Loop through the wind displacement dataframe and drop all rows containing non D1 diaphragms.
#                 windDisplacement_df = windDisplacement_df[
#                     windDisplacement_df["Diaphragm"] == "D1"
#                 ]

#                 # Loop through the wind displacement dataframe and drop all rows containing min. This will be the max dataframe.
#                 max_windDisplacement_df = windDisplacement_df[
#                     windDisplacement_df["StepType"] == "Max"
#                 ]

#                 # Loop through the wind displacement dataframe and drop all rows containing Max. This will be the min dataframe.
#                 min_windDisplacement_df = windDisplacement_df[
#                     windDisplacement_df["StepType"] == "Min"
#                 ]
#                 # Reset indices to ensure that the rows are indexed correctly.
#                 max_windDisplacement_df.reset_index(drop=True, inplace=True)
#                 min_windDisplacement_df.reset_index(drop=True, inplace=True)

#                 # Create new dataframes for min and max overall wind displacement to populate relevant data
#                 overall_min_windDisplacement_df = pd.DataFrame(
#                     columns=[
#                         "Story",
#                         "Elevation (m)",
#                         "Story Height (m)",
#                         "Allowable Limit",
#                         "X Direction Displacement (mm)",
#                         "Y Direction Displacement (mm)",
#                     ]
#                 )
#                 overall_max_windDisplacement_df = pd.DataFrame(
#                     columns=[
#                         "Story",
#                         "Elevation (m)",
#                         "Story Height (m)",
#                         "Allowable Limit",
#                         "X Direction Displacement (mm)",
#                         "Y Direction Displacement (mm)",
#                     ]
#                 )
#                 # Populate columns of new dataframes with appropriate data.
#                 overall_min_windDisplacement_df["Story"] = self.extracts[
#                     "story_heights"
#                 ]["Story"]
#                 overall_max_windDisplacement_df["Story"] = self.extracts[
#                     "story_heights"
#                 ]["Story"]
#                 overall_min_windDisplacement_df["Elevation (m)"] = self.extracts[
#                     "story_heights"
#                 ]["Elevation (m)"]
#                 overall_max_windDisplacement_df["Elevation (m)"] = self.extracts[
#                     "story_heights"
#                 ]["Elevation (m)"]
#                 overall_min_windDisplacement_df["Story Height (m)"] = self.extracts[
#                     "story_heights"
#                 ]["Story Height (m)"]
#                 overall_max_windDisplacement_df["Story Height (m)"] = self.extracts[
#                     "story_heights"
#                 ]["Story Height (m)"]
#                 overall_min_windDisplacement_df["Allowable Limit"] = round(
#                     self.extracts["story_heights"]["Elevation (m)"] * 1000 / 500
#                 )
#                 overall_max_windDisplacement_df["Allowable Limit"] = round(
#                     self.extracts["story_heights"]["Elevation (m)"] * 1000 / 500
#                 )
#                 overall_min_windDisplacement_df[
#                     "X Direction Displacement (mm)"
#                 ] = min_windDisplacement_df["UX"]
#                 overall_max_windDisplacement_df[
#                     "X Direction Displacement (mm)"
#                 ] = max_windDisplacement_df["UX"]
#                 overall_min_windDisplacement_df[
#                     "Y Direction Displacement (mm)"
#                 ] = min_windDisplacement_df["UY"]
#                 overall_max_windDisplacement_df[
#                     "Y Direction Displacement (mm)"
#                 ] = max_windDisplacement_df["UY"]

#                 # Convert column datatypes to float to enable plotting.
#                 overall_max_windDisplacement_df[
#                     "X Direction Displacement (mm)"
#                 ] = overall_max_windDisplacement_df[
#                     "X Direction Displacement (mm)"
#                 ].astype(
#                     float
#                 )
#                 overall_max_windDisplacement_df[
#                     "Y Direction Displacement (mm)"
#                 ] = overall_max_windDisplacement_df[
#                     "Y Direction Displacement (mm)"
#                 ].astype(
#                     float
#                 )
#                 overall_min_windDisplacement_df[
#                     "X Direction Displacement (mm)"
#                 ] = overall_min_windDisplacement_df[
#                     "X Direction Displacement (mm)"
#                 ].astype(
#                     float
#                 )
#                 overall_min_windDisplacement_df[
#                     "Y Direction Displacement (mm)"
#                 ] = overall_min_windDisplacement_df[
#                     "Y Direction Displacement (mm)"
#                 ].astype(
#                     float
#                 )

#                 # Take minimum values and make absolute to enable plotting.
#                 overall_min_windDisplacement_df[
#                     "X Direction Displacement (mm)"
#                 ] = overall_min_windDisplacement_df[
#                     "X Direction Displacement (mm)"
#                 ].abs()
#                 overall_min_windDisplacement_df[
#                     "Y Direction Displacement (mm)"
#                 ] = overall_min_windDisplacement_df[
#                     "Y Direction Displacement (mm)"
#                 ].abs()

#                 # Append the overall max wind displacement and overall min wind displacement to the table attribute.
#                 self.tables["overall_wind_displacement_max"].append(
#                     overall_max_windDisplacement_df
#                 )
#                 self.tables["overall_wind_displacement_min"].append(
#                     overall_min_windDisplacement_df
#                 )
#             else:
#                 # Reset all the load cases and combinations.
#                 Extraction.clear_combos(SapModel)

#                 # Grab Load case rather than load combination.
#                 SapModel.DatabaseTables.SetLoadCasesSelectedForDisplay(  # type: ignore
#                     [combo[1]]
#                 )
#                 SapModel.DatabaseTables.SetOutputOptionsForDisplay(  # type: ignore
#                     IsUserBaseReactionLocation=False,
#                     UserBaseReactionX=False,
#                     UserBaseReactionY=False,
#                     UserBaseReactionZ=False,
#                     IsAllModes=False,
#                     StartMode=1,
#                     EndMode=12,
#                     IsAllBucklingModes=False,
#                     StartBucklingMode=1,
#                     EndBucklingMode=6,
#                     MultistepStatic=1,
#                     NonlinearStatic=1,
#                     ModalHistory=1,
#                     DirectHistory=1,
#                     Combo=1,
#                 )
#                 # Grab the diaphragm center of mass displacements table.
#                 mass_displacement_table = SapModel.DatabaseTables.GetTableForDisplayArray("Diaphragm Center Of Mass Displacements", GroupName="")  # type: ignore

#                 # Extract the column headings and number of rows from the table. This needs to be done as the data is currently an array.
#                 cols = mass_displacement_table[2]
#                 num_rows = mass_displacement_table[3]

#                 # Input data into array split.
#                 table_data = np.array_split(mass_displacement_table[4], num_rows)

#                 # Create wind displacement dataframe.
#                 windDisplacement_df = pd.DataFrame(table_data)
#                 windDisplacement_df.columns = cols

#                 # Loop through the wind displacement dataframe and drop all rows containing non D1 diaphragms.
#                 windDisplacement_df = windDisplacement_df[
#                     windDisplacement_df["Diaphragm"] == "D1"
#                 ]

#                 # Loop through the wind displacement dataframe and drop all rows containing min. This will be the max dataframe.
#                 max_windDisplacement_df = windDisplacement_df[
#                     windDisplacement_df["StepType"] == "Max"
#                 ]

#                 # Loop through the wind displacement dataframe and drop all rows containing Max. This will be the min dataframe.
#                 min_windDisplacement_df = windDisplacement_df[
#                     windDisplacement_df["StepType"] == "Min"
#                 ]

#                 # Reset indices to ensure that the rows are indexed correctly.
#                 max_windDisplacement_df.reset_index(drop=True, inplace=True)
#                 min_windDisplacement_df.reset_index(drop=True, inplace=True)

#                 # Create new dataframes for min and max overall wind displacement to populate relevant data
#                 overall_min_windDisplacement_df = pd.DataFrame(
#                     columns=[
#                         "Story",
#                         "Elevation (m)",
#                         "Story Height (m)",
#                         "Allowable Limit",
#                         "X Direction Displacement (mm)",
#                         "Y Direction Displacement (mm)",
#                     ]
#                 )
#                 overall_max_windDisplacement_df = pd.DataFrame(
#                     columns=[
#                         "Story",
#                         "Elevation (m)",
#                         "Story Height (m)",
#                         "Allowable Limit",
#                         "X Direction Displacement (mm)",
#                         "Y Direction Displacement (mm)",
#                     ]
#                 )

#                 # Populate columns of new dataframes with appropriate data.
#                 overall_min_windDisplacement_df["Story"] = self.extracts[
#                     "story_heights"
#                 ]["Story"]
#                 overall_max_windDisplacement_df["Story"] = self.extracts[
#                     "story_heights"
#                 ]["Story"]
#                 overall_min_windDisplacement_df["Elevation (m)"] = self.extracts[
#                     "story_heights"
#                 ]["Elevation (m)"]
#                 overall_max_windDisplacement_df["Elevation (m)"] = self.extracts[
#                     "story_heights"
#                 ]["Elevation (m)"]
#                 overall_min_windDisplacement_df["Story Height (m)"] = self.extracts[
#                     "story_heights"
#                 ]["Story Height (m)"]
#                 overall_max_windDisplacement_df["Story Height (m)"] = self.extracts[
#                     "story_heights"
#                 ]["Story Height (m)"]
#                 overall_min_windDisplacement_df["Allowable Limit"] = round(
#                     self.extracts["story_heights"]["Elevation (m)"] * 1000 / 500
#                 )
#                 overall_max_windDisplacement_df["Allowable Limit"] = round(
#                     self.extracts["story_heights"]["Elevation (m)"] * 1000 / 500
#                 )
#                 overall_min_windDisplacement_df[
#                     "X Direction Displacement (mm)"
#                 ] = min_windDisplacement_df["UX"]
#                 overall_max_windDisplacement_df[
#                     "X Direction Displacement (mm)"
#                 ] = max_windDisplacement_df["UX"]
#                 overall_min_windDisplacement_df[
#                     "Y Direction Displacement (mm)"
#                 ] = min_windDisplacement_df["UY"]
#                 overall_max_windDisplacement_df[
#                     "Y Direction Displacement (mm)"
#                 ] = max_windDisplacement_df["UY"]

#                 # Convert column datatypes to float to enable plotting.
#                 overall_max_windDisplacement_df[
#                     "X Direction Displacement (mm)"
#                 ] = overall_max_windDisplacement_df[
#                     "X Direction Displacement (mm)"
#                 ].astype(
#                     float
#                 )
#                 overall_max_windDisplacement_df[
#                     "Y Direction Displacement (mm)"
#                 ] = overall_max_windDisplacement_df[
#                     "Y Direction Displacement (mm)"
#                 ].astype(
#                     float
#                 )
#                 overall_min_windDisplacement_df[
#                     "X Direction Displacement (mm)"
#                 ] = overall_min_windDisplacement_df[
#                     "X Direction Displacement (mm)"
#                 ].astype(
#                     float
#                 )
#                 overall_min_windDisplacement_df[
#                     "Y Direction Displacement (mm)"
#                 ] = overall_min_windDisplacement_df[
#                     "Y Direction Displacement (mm)"
#                 ].astype(
#                     float
#                 )

#                 # Take minimum values and make absolute to enable plotting.
#                 overall_min_windDisplacement_df[
#                     "X Direction Displacement (mm)"
#                 ] = overall_min_windDisplacement_df[
#                     "X Direction Displacement (mm)"
#                 ].abs()
#                 overall_min_windDisplacement_df[
#                     "Y Direction Displacement (mm)"
#                 ] = overall_min_windDisplacement_df[
#                     "Y Direction Displacement (mm)"
#                 ].abs()

#                 # Append the overall max wind displacement and overall min wind displacement to the table attribute.
#                 self.tables["overall_wind_displacement_max"].append(
#                     overall_max_windDisplacement_df
#                 )
#                 self.tables["overall_wind_displacement_min"].append(
#                     overall_min_windDisplacement_df
#                 )

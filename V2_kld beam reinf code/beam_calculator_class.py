# import math
# import numpy as np


class Beam:
    """This class aims to obtain the necessary information to calculate the beam
    reinforcement schedule.
    """

    def __init__(self, id):
        """Begin by initializing attributes that define the makeup of a reinforced
        concrete beam.
        """
        self.id = id

    def obtain_id(self):
        """This method loops through the third row of each spreadsheet to obtain a list
        of ETABS ID's.
        """
        etabs_id = self.id.iloc[::3]
        return etabs_id

@staticmethod
def initialise_sap_model() -> object:
    """This static method initialises the ETABS SapModel for other methods to utilise.

    Returns:
        object: The ETABS SapModel object.
    """
    # Create API helper object.
    helper = comtypes.client.CreateObject("ETABSv1.Helper")  # type: ignore
    helper = helper.QueryInterface(comtypes.gen.ETABSv1.cHelper)  # type: ignore
    SapModel = None

    try:
        # Get the current ETABS instance.
        myETABSObject = helper.GetObject("CSI.ETABS.API.ETABSObject")
        # Create SapModel object (ETABS instance)
        SapModel = myETABSObject.SapModel
    except (OSError, comtypes.COMError, AttributeError):  # type: ignore
        print("No running instance of the program found or failed to attach.")

    return SapModel


@staticmethod
def initialise_sap_model() -> object:
    """This static method initialises the ETABS SapModel for other methods to utilise.

    Returns:
        object: The ETABS SapModel object.
    """
    # Create API helper object.
    helper = comtypes.client.CreateObject("ETABSv1.Helper")
    helper = helper.QueryInterface(comtypes.gen.ETABSv1.cHelper)  # type: ignore
    SapModel = None

    try:
        # Get the current ETABS instance.
        myETABSObject = helper.GetObject("CSI.ETABS.API.ETABSObject")
        # Create SapModel object (ETABS instance)
        SapModel = myETABSObject.SapModel
    except (OSError, comtypes.COMError, AttributeError):
        print("No running instance of the program found or failed to attach.")

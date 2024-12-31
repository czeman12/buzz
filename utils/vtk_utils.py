# utils/vtk_utils.py

import vtk


def create_color_map(name: str = "jet") -> vtk.vtkLookupTable:
    """
    Create a VTK lookup table based on the specified color map.

    :param name: Name of the color map ('jet', 'hot', etc.).
    :return: vtkLookupTable instance.
    """
    color_transfer = vtk.vtkLookupTable()
    color_transfer.SetNumberOfTableValues(256)
    color_transfer.Build()

    if name == "jet":
        color_transfer.SetHueRange(0.667, 0.0)  # Blue to red
    elif name == "hot":
        color_transfer.SetHueRange(0.0, 0.0)
        color_transfer.SetSaturationRange(0.0, 0.0)
        color_transfer.SetValueRange(0.0, 1.0)
        color_transfer.SetRampToLinear()
    else:
        # Default to jet
        color_transfer.SetHueRange(0.667, 0.0)

    return color_transfer


def convert_step_to_stl(step_file: str, stl_file: str):
    """
    Convert a STEP (.stp/.step) file to an STL file using pythonOCC.

    :param step_file: Path to the input STEP file.
    :param stl_file: Path to the output STL file.
    """
    from OCC.Core.STEPControl import STEPControl_Reader
    from OCC.Core.StlAPI import StlAPI_Writer
    from OCC.Core.IFSelect import IFSelect_RetDone

    reader = STEPControl_Reader()
    status = reader.ReadFile(step_file)

    if status == IFSelect_RetDone:
        reader.TransferRoots()
        shape = reader.OneShape()
        writer = StlAPI_Writer()
        writer.SetASCIIMode(True)
        writer.Write(shape, stl_file)
    else:
        raise ValueError(f"Failed to read STEP file: {step_file}")

#***************************************************************************
#*    Copyright (C) 2023 
#*    This library is free software
#***************************************************************************
import inspect
import os
import FreeCADGui
import FreeCAD

class PipeFittingsShowCommand:
    def GetResources(self):
        file_path = inspect.getfile(inspect.currentframe())
        module_path=os.path.dirname(file_path)
        return { 
          'Pixmap': os.path.join( module_path,"icons", "PipeFittings.svg"),
          'MenuText': "PipeFittings",
          'ToolTip': "Show/Hide PipeFittings"}

    def IsActive(self):
        import PipeFittings
        PipeFittings
        print('eee')
        return True

    def Activated(self):
        try:
          import PipeFittings
          PipeFittings.main.d.show()
        except Exception as e:
          FreeCAD.Console.PrintError(str(e) + "\n")

        file_path = inspect.getfile(inspect.currentframe())
        module_path=os.path.dirname(file_path)

    def IsActive(self):
        import PipeFittings
        return not FreeCAD.ActiveDocument is None

class PipeFittingsWB(FreeCADGui.Workbench):
    def __init__(self):
        file_path = inspect.getfile(inspect.currentframe())
        module_path=os.path.dirname(file_path)
        self.__class__.Icon = os.path.join( module_path,"icons", "PipeFittings.svg")
        self.__class__.MenuText = "PipeFittings"
        self.__class__.ToolTip = "PipeFittings by Pascal"

    def Initialize(self):
        self.commandList = ["PipeFittings_Show"]
        self.appendToolbar("&PipeFittings", self.commandList)
        self.appendMenu("&PipeFittings", self.commandList)

    def Activated(self):
        import PipeFittings
        PipeFittings
        return

    def Deactivated(self):
        return

    def ContextMenu(self, recipient):
        return

    def GetClassName(self): 
        return "Gui::PythonWorkbench"
FreeCADGui.addWorkbench(PipeFittingsWB())
FreeCADGui.addCommand("PipeFittings_Show", PipeFittingsShowCommand())

#***************************************************************************
#*    Copyright (C) 2023 
#*    This library is free software
#***************************************************************************

import os
import FreeCADGui
import FreeCAD

class PipeFittingsShowCommand:
    def GetResources(self):
        from Init import module_path
        #module_path = os.path.dirname(os.path.abspath(__file__))
        #print(os.path)
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

    def IsActive(self):
        import PipeFittings
        #SteelStructure
        return not FreeCAD.ActiveDocument is None

class PipeFittingsWB(FreeCADGui.Workbench):
    def __init__(self):
        from Init import module_path
        print(module_path)
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

freeCadVersion = int(FreeCAD.Version()[1])
pythonVersion = int(sys.version[0:1])

FreeCADGui.addWorkbench(PipeFittingsWB())
FreeCADGui.addCommand("PipeFittings_Show", PipeFittingsShowCommand())

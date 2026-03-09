from abaqusGui import *
from abaqusConstants import ALL
import osutils, os


###########################################################################
# Class definition
###########################################################################

class PD_Comp_P_plugin(AFXForm):

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def __init__(self, owner):
        
        # Construct the base class.
        #
        AFXForm.__init__(self, owner)
        self.radioButtonGroups = {}

        self.cmd = AFXGuiCommand(mode=self, method='createPDPlateFunction',
            objectName='PD_Plate_Plug', registerQuery=False)
        pickedDefault = ''
        self.pathdKw = AFXStringKeyword(self.cmd, 'pathd', True, '')
        self.widthKw = AFXFloatKeyword(self.cmd, 'width', True)
        self.heightKw = AFXFloatKeyword(self.cmd, 'height', True)
        self.thicknessKw = AFXFloatKeyword(self.cmd, 'thickness', True)
        self.nxKw = AFXIntKeyword(self.cmd, 'nx', True)
        self.nyKw = AFXIntKeyword(self.cmd, 'ny', True)
        self.EKw = AFXFloatKeyword(self.cmd, 'E', True)
        self.NuKw = AFXFloatKeyword(self.cmd, 'Nu', True)
        self.FKw = AFXFloatKeyword(self.cmd, 'F', True)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def getFirstDialog(self):

        import pD_Comp_PDB
        return pD_Comp_PDB.PD_Comp_PDB(self)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def doCustomChecks(self):

        # Try to set the appropriate radio button on. If the user did
        # not specify any buttons to be on, do nothing.
        #
        for kw1,kw2,d in self.radioButtonGroups.values():
            try:
                value = d[ kw1.getValue() ]
                kw2.setValue(value)
            except:
                pass
        return True

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def okToCancel(self):

        # No need to close the dialog when a file operation (such
        # as New or Open) or model change is executed.
        #
        return False

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Register the plug-in
#
thisPath = os.path.abspath(__file__)
thisDir = os.path.dirname(thisPath)

toolset = getAFXApp().getAFXMainWindow().getPluginToolset()
toolset.registerGuiMenuButton(
    buttonText='PD Plate Plugin', 
    object=PD_Comp_P_plugin(toolset),
    messageId=AFXMode.ID_ACTIVATE,
    icon=None,
    kernelInitString='import PD_Plate_Plug',
    applicableModules=ALL,
    version='N/A',
    author='N/A',
    description='N/A',
    helpUrl='N/A'
)

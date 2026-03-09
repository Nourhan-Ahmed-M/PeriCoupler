from abaqusConstants import *
from abaqusGui import *
from kernelAccess import mdb, session
import os

thisPath = os.path.abspath(__file__)
thisDir = os.path.dirname(thisPath)


###########################################################################
# Class definition
###########################################################################

class PD_Comp_PDB(AFXDataDialog):

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def __init__(self, form):

        # Construct the base class.
        #

        AFXDataDialog.__init__(self, form, 'PD Plate Dialog Box',
            self.OK|self.CANCEL, DIALOG_ACTIONS_SEPARATOR)
            

        okBtn = self.getActionButton(self.ID_CLICKED_OK)
        okBtn.setText('OK')
            
        GroupBox_1 = FXGroupBox(p=self, text='Specify Path directory', opts=FRAME_GROOVE)
        AFXTextField(p=GroupBox_1, ncols=12, labelText='Path Directory:', tgt=form.pathdKw, sel=0)
        GroupBox_2 = FXGroupBox(p=self, text='Geometric Parameters (Float)', opts=FRAME_GROOVE)
        AFXTextField(p=GroupBox_2, ncols=12, labelText='Width(m):', tgt=form.widthKw, sel=0)
        AFXTextField(p=GroupBox_2, ncols=12, labelText='Height(m):', tgt=form.heightKw, sel=0)
        AFXTextField(p=GroupBox_2, ncols=12, labelText='Thickness(m):', tgt=form.thicknessKw, sel=0)
        GroupBox_6 = FXGroupBox(p=self, text='Discretization Parameters(Integer)', opts=FRAME_GROOVE)
        AFXTextField(p=GroupBox_6, ncols=12, labelText='Material points in x :', tgt=form.nxKw, sel=0)
        AFXTextField(p=GroupBox_6, ncols=12, labelText='Material points in y :', tgt=form.nyKw, sel=0)
        GroupBox_7 = FXGroupBox(p=self, text='Material Properties', opts=FRAME_GROOVE)
        AFXTextField(p=GroupBox_7, ncols=12, labelText='E(Pa):', tgt=form.EKw, sel=0)
        AFXTextField(p=GroupBox_7, ncols=12, labelText='Poissons Ratio:', tgt=form.NuKw, sel=0)
        GroupBox_8 = FXGroupBox(p=self, text='Load', opts=FRAME_GROOVE)
        AFXTextField(p=GroupBox_8, ncols=12, labelText='Force(N):', tgt=form.FKw, sel=0)
        HFrame_1 = FXHorizontalFrame(p=self, opts=0, x=0, y=0, w=0, h=0,
            pl=0, pr=0, pt=0, pb=0)
        l = FXLabel(p=HFrame_1, text='\xa9 2025 Nourhan Ahmed', opts=JUSTIFY_LEFT)
        HFrame_2 = FXHorizontalFrame(p=self, opts=0, x=0, y=0, w=0, h=0,
            pl=0, pr=0, pt=0, pb=0)
        l = FXLabel(p=HFrame_2, text='namaahmed@mun.ca', opts=JUSTIFY_LEFT)

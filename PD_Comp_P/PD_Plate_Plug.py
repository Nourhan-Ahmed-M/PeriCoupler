# Starting new analysis msg 
print('*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*\n'*3)
print('Starting New Analysis Linear Elastic Behavior\n'*3)  
print('*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*\n'*3)
# Include essential Python libraries 
import fileinput
import glob
import os
import re
import numpy
import random
import csv
from itertools import count
from numpy import array
import datetime
#----------------------------------------------------------------#
# Import Essential libraries from Abaqus
from abaqus import *
from abaqusConstants import *
import __main__
#----------------------------------------------------------------#
# Import CAE libraries
import section
import regionToolset
import displayGroupMdbToolset as dgm
import part
import material
import assembly
import optimization
import step
import interaction
import load
import mesh
import job
import sketch
import visualization
import xyPlot
import displayGroupOdbToolset as dgo
import connectorBehavior
import time
#----------------------------------------------------------------#
def createPDPlateFunction(pathd,width,height,thickness,nx,ny,E,F,Nu):
 #----------------------------------------------------------------#
 # Create new model
 #----------------------------------------------------------------#
    Mdb()
    model = mdb.Model(name='Model-1')
#----------------------------------------------------------------#
# Define Geometric Parameters
#----------------------------------------------------------------#
    L_x=width
    L_y=height
    t=thickness
    F=F                                   # Force [N]
    F_1=F/2.0
    F_2=F/2.0
    E=E                                 # Young's Modulus [Pa]
    Nu=Nu                                  # Poisson's Ratio
    
#----------------------------------------------------------------#
# Discretization Parameters
#----------------------------------------------------------------#
    N_x= nx                                 # Number of Material Points in x
    n_x= N_x-1.0                              # Number of Elements in x
    N_y= ny                                 # Number of Material Points in y
    n_y= N_y-1.0                              # Number of Elements in y

    Nr=3.0                                    # each material point interact with 3 points ion the horizon 
    Nr_n=Nr+1     
    ns_b_x=round(n_x/Nr)                      # number of elements selected in block in x
    ns_x=ns_b_x*Nr                            # total number of elements selected in x

    ns_b_y=round(n_y/Nr)                      # number of elements selected in block in y
    ns_y=ns_b_y*Nr                            # total number of elements selected in y

    f=F/ns_y                                  # force per node

    Nt_x=ns_x+1.0                             # total number of material points selected in x
    Nt_y=ns_y+1.0                             # total number of material points selected in y

    N_bx= ns_x/Nr                             # number of blocks in x
    N_by= ns_y/Nr                             # number of blocks in x

    dx= L_x/(Nt_x-1.0)                         # Spacing between material points in x direction 
    dy= L_y/(Nt_y-1.0)                         # Spacing between material points in y direction  

    delta= Nr*dx                            # Horizon
    delta_y=Nr*dy 

    Vp= dx*dx*dx

    N_tot=Nt_x*Nt_y

    Nr_tot=(Nr_n)*(Nr_n)

#----------------------------------------------------------------#
# Mapping Parameters
#----------------------------------------------------------------#

    Micro_c= 6.0*E/((1.0-Nu)*pi*t*delta**3.0)     # Micro Modulus [N/m^6] 2D plane stress

    A_P= (Vp*Vp)**(1.0/3.0)                      # Mapped Area [m^2]
    E_P= Micro_c*(Vp*Vp)**(2.0/3.0)              # Mapped E

    SPD_coef=(1.0/6.0)*pi*Micro_c*t*delta**3.0  # Mapping stress coeffecient

#Critical Stretch
    Segma_a=F/(L_y*t)                            # ultimate stress
    S_Y=6.0*Segma_a/(pi*Micro_c*delta**4.0)      # Yield strain
    Segma_Y=S_Y*E_P                              # Yield stress
    Go=0.5*S_Y*Segma_Y                           # Energy release rate
    So=(4.0*Go/(Micro_c*t*delta**4.0))**0.5      # Critical strain 2D    
    #----------------------------------------------------------------#
# Create Material points 
#----------------------------------------------------------------#
# Create Coordinates
    X_cord = -dx
    Y_cord = -dy
    XY_cord = []
    i=1
    j=1
    n=1
    list_X = []
    list_Y = []
    Nodes_XY = [] 
    Nt_int_x=int(Nt_x)
    Nt_int_y=int(Nt_y)
    N_tot_int=int(N_tot)
   
    for i in range (Nt_int_x):    
        X_cord=X_cord+dx
        locals()["X_cord" + repr(i+1)] = X_cord
        C_X = float(locals()["X_cord" + repr(i+1)])
        Y_cord=-dy
    
        for j in range(Nt_int_y):
            Y_cord = Y_cord + dy
            locals()["Y_cord" + repr(j+1)] = Y_cord
            C_Y = float(locals()["Y_cord" + repr(j+1)])
            point_num_cln = repr(i+1)+'-'+repr(j+1)
            print (['X-->'+ point_num_cln],X_cord)
            list_X.append(X_cord)
            print (['Y-->'+ point_num_cln],Y_cord)
            list_Y.append(Y_cord)
            point = (X_cord,Y_cord)
            Nodes_XY.append(point)
            j += 1	
        i += 1 

#----------------------------------------------------------------#
# Construct grid points (Material points in length of horizon)
#----------------------------------------------------------------#
# Create Coordinates
    xcord = -dx
    ycord = -dy
    xycord = []
    listx = []
    listy = []
    Nodes_vect = []            # all material points in horizon grid
    Nr_int=int(Nr_n)
    Nr_tot_int=int(Nr_tot)
    for i in range (Nr_int):    
        xcord=xcord+dx
        locals()["xcord" + repr(i+1)] = xcord
        CX = float(locals()["xcord" + repr(i+1)])     
        ycord=-dy   
        for j in range(Nr_int):
            ycord = ycord + dy
            locals()["ycord" + repr(j+1)] = ycord
            CY = float(locals()["ycord" + repr(j+1)])
            point_num=repr(i+1)+'-'+repr(j+1)
            print (['x-->'+point_num],xcord)
            listx.append(xcord)
            print (['y-->'+point_num],ycord)
            listy.append(ycord)
            grid = (xcord,ycord)
            Nodes_vect.append(grid)
                                                    
            j += 1	
           
        i += 1 
    
    sketch = model.ConstrainedSketch(name='Sketch-1', sheetSize=10000.0)
    Line_num = 0.0   
    for i in range(Nr_tot_int):
        for j in range(i+1, Nr_tot_int):        
            dist = ((Nodes_vect[i][0]-Nodes_vect[j][0])**2 + (Nodes_vect[i][1]-Nodes_vect[j][1])**2)**0.5
            if dist <= delta:
            
                sketch.Line(point1=(Nodes_vect[i][0], Nodes_vect[i][1]), point2=(Nodes_vect[j][0], Nodes_vect[j][1]))             
                Line_num=Line_num+1.0                      
            
            j += 1 
        i += 1 
    
    N_1=int(N_bx)
    N_2=int(N_by)
    geom_list = []
    for geom_id in sketch.geometry.keys():
        geom_list.append(sketch.geometry[geom_id])
    sketch.linearPattern(geomList=geom_list, vertexList=(), number1=N_1, spacing1=delta, angle1=0.0, number2=N_2, spacing2=delta, angle2=90.0)


        
    part = model.Part(name='Part-1', dimensionality=THREE_D, type=DEFORMABLE_BODY)
    part.Wire(sketch=sketch)
    session.viewports['Viewport: 1'].setValues(displayedObject=part)   
    print ('Part Created Successfully')
#----------------------------------------------------------------#
# Create Material 
#----------------------------------------------------------------#
    material_1 =model.Material(name='Material-1')
    material_1.Elastic(table=((E_P, Nu), ))


#----------------------------------------------------------------#
# Create Section
#----------------------------------------------------------------#
    model.TrussSection(name='Section-1', material='Material-1', area=A_P)
#----------------------------------------------------------------#
# Assign Section
#----------------------------------------------------------------#

    edges=part.edges.getByBoundingBox(xMin= 0.0, yMin= 0.0, xMax=L_x, yMax=  L_y)
    region = part.Set(edges=edges, name='Set-1')                    
    part.SectionAssignment(region=region, sectionName='Section-1', offset=0.0)               
    part.assignBeamSectionOrientation(region=region, method=N1_COSINES, n1=(0.0, 0.0, -1.0))

#----------------------------------------------------------------#
# Create Assembly
#----------------------------------------------------------------#
    assembly = model.rootAssembly
    session.viewports['Viewport: 1'].setValues(displayedObject=assembly)
    session.viewports['Viewport: 1'].assemblyDisplay.setValues(optimizationTasks=OFF, geometricRestrictions=OFF, stopConditions=OFF)        
    assembly.DatumCsysByDefault(CARTESIAN)
# Create Instances
    instance = assembly.Instance(name='Part-1-1', part=part, dependent=ON)
    session.viewports['Viewport: 1'].assemblyDisplay.setValues(adaptiveMeshConstraints=ON)
#----------------------------------------------------------------#
# Create Steps
#----------------------------------------------------------------#
    model.StaticStep(name='Step-1', previous='Initial', timePeriod=1.0, initialInc=0.1, minInc=1e-05, maxInc=0.1)
# Edit field output request and include NT and TEMP output variables
    model.fieldOutputRequests['F-Output-1'].setValues(timeInterval=0.01)
    model.fieldOutputRequests['F-Output-1'].setValues(variables=('S', 
                                                                             'PE', 
                                                                             'PEEQ', 
                                                                             'PEMAG', 
                                                                             'LE', 
                                                                             'U', 
                                                                             'RF', 
                                                                             'CF', 
                                                                             'CSTRESS', 
                                                                             'CDISP', 
                                                                             'NT', 
                                                                             'TEMP'))
                                                                             



    print('Create B.C')
#----------------------------------------------------------------#
# Boundary Conditions 
#----------------------------------------------------------------#


    v1 = assembly.instances['Part-1-1'].vertices
    left_end = v1.getByBoundingBox(xMin= 0.0, yMin= 0.0, xMax=0.0, yMax=  L_y)
    region_left = assembly.Set(vertices=left_end, name='Set-2')
    model.EncastreBC(name='BC-1', createStepName='Step-1', region=region_left, localCsys=None) 


    print('Create Load')
#----------------------------------------------------------------#
# Loads
#----------------------------------------------------------------#
    v1 = assembly.instances['Part-1-1'].vertices
    right_end =v1.getByBoundingBox(xMin= L_x, yMin= 0.0, xMax=L_x, yMax=  L_y)
    region_right = assembly.Set(vertices=right_end, name='Set-3')
    model.ConcentratedForce(name='Load-1', createStepName='Step-1', region=region_right, cf1=f, distributionType=UNIFORM, field='', localCsys=None)   

    print('Create Mesh')              

#----------------------------------------------------------------#
# Mesh
#----------------------------------------------------------------#
    session.viewports['Viewport: 1'].setValues(displayedObject=part)
    session.viewports['Viewport: 1'].partDisplay.setValues(sectionAssignments=OFF, engineeringFeatures=OFF, mesh=ON)        
    session.viewports['Viewport: 1'].partDisplay.meshOptions.setValues( meshTechnique=ON)
# Select Element Type 
    elemType1 = mesh.ElemType(elemCode=T3D2, elemLibrary=STANDARD)
    pickedRegions =(edges, )
    part.setElementType(regions=pickedRegions, elemTypes=(elemType1, ))

# Generate Mesh             
    part.seedPart(size=100, deviationFactor=0.1, minSizeFactor=0.1)
    part.generateMesh()

#----------------------------------------------------------------#
# Create Job
#----------------------------------------------------------------#
    assembly.regenerate()
    session.viewports['Viewport: 1'].setValues(displayedObject=assembly)
    session.viewports['Viewport: 1'].assemblyDisplay.meshOptions.setValues(meshTechnique=OFF)
    session.viewports['Viewport: 1'].assemblyDisplay.setValues(adaptiveMeshConstraints=OFF)

    JobName = 'Script_PD_Horizon_Plugin_Job'  

    if JobName in mdb.jobs.keys():
        del mdb.jobs[JobName]

    mdb.Job(name=JobName, model='Model-1', description='', type=ANALYSIS, 
        atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=90, 
        memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True, 
        explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=OFF, 
        modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='', 
        scratch='', resultsFormat=ODB, multiprocessingMode=DEFAULT, numCpus=1, 
        numGPUs=0)
        
#----------------------------------------------------------------#
# Set the viewport to show the assembly
#----------------------------------------------------------------#
    session.viewports['Viewport: 1'].setValues(displayedObject=assembly)
    session.viewports['Viewport: 1'].assemblyDisplay.setValues(loads=OFF, bcs=OFF, predefinedFields=OFF, connectors=OFF)

#----------------------------------------------------------------#
# Submit the job
#----------------------------------------------------------------#

    mdb.jobs[JobName].submit(consistencyChecking=OFF)
# Wait for completion
    mdb.jobs[JobName].waitForCompletion()

  #----------------------------------------------------------------#
# View results
#----------------------------------------------------------------#
    P_Odb = JobName +'.odb'
    Odb_Path   = pathd 
    P_Odb_Path = Odb_Path+P_Odb

    session.viewports['Viewport: 1'].setValues(displayedObject=assembly) 
    session.mdbData.summary()
    CurrODB = session.openOdb(name=P_Odb_Path ,readOnly=False)
    session.viewports['Viewport: 1'].setValues(displayedObject=CurrODB) 
    #----------------------------------------------------------------#
# Modify stress

    session.mdbData.summary()
    odb = session.odbs[P_Odb_Path]
    session.viewports['Viewport: 1'].setValues(displayedObject=odb)
    s1f100_E = session.odbs[P_Odb_Path].steps['Step-1'].frames[100].fieldOutputs['E']
    tmpField = s1f100_E*SPD_coef
    currentOdb = session.odbs[P_Odb_Path]
    scratchOdb = session.ScratchOdb(odb=currentOdb)
    sessionStep = scratchOdb.Step(name='Session Step', 
        description='Step for Viewer non-persistent fields', domain=TIME, 
        timePeriod=1.0)
    sessionFrame = sessionStep.Frame(frameId=0, frameValue=0.0, 
        description='Session Frame')
    sessionField = sessionFrame.FieldOutput(name='PD_stress', 
        description='s1f100_E*SPD_coef', field=tmpField)


    frame = session.odbs[P_Odb_Path].steps['Step-1'].frames[100]
    tempField = session.scratchOdbs[P_Odb_Path].steps['Session Step'].frames[0].fieldOutputs['PD_stress']

    frame.FieldOutput(name='PD_stress', description='s1f100_E*SPD_coef',field=tempField) 
        
    session.odbs[P_Odb_Path].save()
        
    session.viewports['Viewport: 1'].odbDisplay.setPrimaryVariable(
        variableLabel='PD_stress', outputPosition=INTEGRATION_POINT, 
        refinement=(INVARIANT, 'Max. In-Plane Principal'), )

    print ('Done')
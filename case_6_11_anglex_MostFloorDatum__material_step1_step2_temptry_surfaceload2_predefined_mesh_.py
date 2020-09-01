from abaqus import *
from abaqusConstants import *
from caeModules import *
import material
#part
if mdb.models.has_key('myModel'):
    m = mdb.models['myModel']
else:
    m = mdb.Model(name ='myModel')
Se = m.ConstrainedSketch(name='Extrude',sheetSize=10.0)
g,c = Se.geometry,Se.constraints
Se.setPrimaryObject(option=STANDALONE)
line1 = Se.Line(point1 = (0,0),point2 = (1.0,0))
line2 = Se.Line(point1 = (1.0,0),point2 = (1,0.4))
line3 = Se.Line(point1 = (1,0.4),point2 = (0.0,0.4))
line4 = Se.Line(point1 = (0.0,0.4),point2 =(0.0,0))
Se.PerpendicularConstraint(entity1 =line3,entity2 =line4)
Se.autoDimension(objectList=(line4,))
Se.unsetPrimaryObject()
p1 = mdb.models['myModel'].Part(name='Part-1',dimensionality=THREE_D,type = DEFORMABLE_BODY)
p1.BaseSolidExtrude(sketch=Se, depth=1)
vp = session.viewports['Viewport: 1']
p1 = mdb.models['myModel'].parts['Part-1']
vp.setValues(displayedObject=p1)
print ("part is ok")
#feature
es = p1.edges
jm=10
im=10
mm=5
for j in range(1,jm):
    pt1=p1.DatumPointByCoordinate(coords=(1.0*j/jm,0,1))
    pt2=p1.DatumPointByCoordinate(coords=(1.0*j/jm,0.4,1))
    pt3=p1.DatumPointByCoordinate(coords=(1.0*j/jm,0.4,0))
    d =p1.datums
    PL1= p1.DatumPlaneByThreePoints(point1=d[pt1.id],point2=d[pt2.id],point3=d[pt3.id])
    cs = p1.cells
    p1.PartitionCellByDatumPlane(cells=cs,datumPlane=d[PL1.id]) 
    print(j)
for i in range(1,im):
    pt1=p1.DatumPointByCoordinate(coords=(0,0.4*i/im,0))
    pt2=p1.DatumPointByCoordinate(coords=(1,0.4*i/im,0))
    pt3=p1.DatumPointByCoordinate(coords=(1,0.4*i/im,1))
    d =p1.datums
    PL2= p1.DatumPlaneByThreePoints(point1=d[pt1.id],point2=d[pt2.id],point3=d[pt3.id])
    cy = p1.cells
    p1.PartitionCellByDatumPlane(cells=cy,datumPlane=d[PL2.id])
    print(i)
for m in range(1,mm):
    pt1=p1.DatumPointByCoordinate(coords=(0,0,1.0*m/mm))
    pt2=p1.DatumPointByCoordinate(coords=(0,0.4,1.0*m/mm))
    pt3=p1.DatumPointByCoordinate(coords=(1,0.4,1.0*m/mm))
    d =p1.datums
    PL3= p1.DatumPlaneByThreePoints(point1=d[pt1.id],point2=d[pt2.id],point3=d[pt3.id])
    cm = p1.cells
    p1.PartitionCellByDatumPlane(cells=cm,datumPlane=d[PL3.id])
    print(m)
print ("feature is ok")

#mesh
elemType1 = mesh.ElemType(elemCode=DC3D8, elemLibrary=STANDARD, 
    kinematicSplit=AVERAGE_STRAIN, secondOrderAccuracy=OFF, 
    hourglassControl=DEFAULT, distortionControl=DEFAULT)
p1.seedPart(size=0.1, deviationFactor=0.1)
c1 = p1.cells
p1.setElementType(regions=(c1,), elemTypes=(elemType1, ))
p1.generateMesh()
#material
mdb.models['myModel'].Material(name='Lv')
mdb.models['myModel'].materials['Lv'].Density(table=((2.81e-06, ), ))
mdb.models['myModel'].materials['Lv'].SpecificHeat(table=((8.54e+08, ), ))
mdb.models['myModel'].materials['Lv'].Conductivity(table=((115000, ), ))
mdb.models['myModel'].HomogeneousSolidSection(name='Section-Lv',material='Lv',thickness=None)
c1 = p1.cells
region1 = regionToolset.Region(cells=c1)
p1.SectionAssignment(region = region1,sectionName = 'Section-Lv',offset =0.0,offsetType = MIDDLE_SURFACE,offsetField='',thicknessAssignment= FROM_SECTION)

print ("material is ok")
#Assembly
a = mdb.models['myModel'].rootAssembly
p11 = a.Instance(name = 'Part-1-1',part = p1,dependent = ON)
#Create the step-1
import step
heatModel = mdb.models['myModel']
moveTime=10
heatModel.HeatTransferStep(name='Heating Step', previous='Initial', 
        timePeriod=moveTime, maxNumInc=10000, initialInc=moveTime*0.005, 
        minInc=moveTime*1e-8, maxInc=moveTime*0.03, deltmx=200.0)
fOR =mdb.models['myModel'].fieldOutputRequests['F-Output-1']
fOR.setValues(variables=('NT','HFL'))
#mdb.models['myModel'].fieldOutputRequests.changeKey(fromName='F-Output-1',toName='Selected Field Outputs')
#mdb.models['myModel'].fieldOutputRequests['Selected Field Outputs'].setValues(variables=('NT',))
#load 
import load 
ipart = heatModel.rootAssembly.instances['Part-1-1']
allsetName = 'Set-all'
allset = heatModel.rootAssembly.Set(cells= ipart.cells,name = allsetName)
heatModel.Temperature(name='Predefined',createStepName = 'Initial',region = allset,magnitudes = 20)
s1 = a.instances['Part-1-1'].faces
side1Faces1 = s1.findAt(((0.155,0.0,0.155),),((0.155,0.0,0.205),),((0.205,0.0,0.205),))
region = a.Surface(side1Faces= side1Faces1,name ='Surf-1')
mdb.models['myModel'].SurfaceHeatFlux(name = 'heatload', createStepName = 'Heating Step', region=region,magnitude = 400000)
heatModel.setValues(absoluteZero = -273.15,stefanBoltzmann=5.67E-8)
print ("step1 is ok")

            
#Create the step-2
import step
heatModel = mdb.models['myModel']
moveTime=10
heatModel.HeatTransferStep(name='Heating Step2', previous='Heating Step', 
        timePeriod=moveTime, maxNumInc=10000, initialInc=moveTime*0.005, 
        minInc=moveTime*1e-8, maxInc=moveTime*0.03, deltmx=200.0)
mdb.models['myModel'].FieldOutputRequest(name ='F-Output-step_2',numIntervals=1,createStepName='Heating Step2',variables=('NT','HFL'))
#fOR2.setValues(variables=('NT',))
#mdb.models['myModel'].fieldOutputRequests.changeKey(fromName='F-Output-1',toName='Selected Field Outputs2')
#mdb.models['myModel'].fieldOutputRequests['Selected Field Outputs2'].setValues(variables=('NT',))
#load 
import load 
s1 = a.instances['Part-1-1'].faces
side1Faces1 = s1.findAt(((0.155,0.0,0.155),),((0.155,0.0,0.205),),((0.205,0.0,0.205),))
region = a.Surface(side1Faces= side1Faces1,name ='Surf-1')
mdb.models['myModel'].SurfaceHeatFlux(name = 'heatload2', createStepName = 'Heating Step2', region=region,magnitude = 300000)
heatModel.setValues(absoluteZero = -273.15,stefanBoltzmann=5.67E-8)
print ("step2 is ok")
            
#Creat the job
import job
mdb.Job(name ='HeatTransferJob',model ='myModel',type = ANALYSIS)
mdb.jobs['HeatTransferJob'].submit(consistencyChecking=OFF)
mdb.jobs['HeatTransferJob'].waitForCompletion()
"""
#extract tempfor x in range(1,jm+1,1):#x*jm
    for y in range(1,im+1,1):#y*10im
        for z in range(1,mm+1,1):#z*m
            x2=float(x)/jm
            y2=y*(0.4/im)
            z2=float(z)/mm
            print(x2,y2,z2)        
            dian1 = mdb.models['myModel'].parts['Part-1'].vertices.findAt(x,y,z)
            dian2 = mdb.models['myModel'].parts['Part-1'].vertices.findAt(x,y-1/im,z)
            dian3 = mdb.models['myModel'].parts['Part-1'].vertices.findAt(x-1/jm,y-1/im,z)
            dian4 = mdb.models['myModel'].parts['Part-1'].vertices.findAt(x-1/jm,y,z)
            dian5 = mdb.models['myModel'].parts['Part-1'].vertices.findAt(x,y,z-1/mm)
            dian6 = mdb.models['myModel'].parts['Part-1'].vertices.findAt(x,y-1/im,z-1/mm)
            dian7 = mdb.models['myModel'].parts['Part-1'].vertices.findAt(x-1/jm,y-1/im,z-1/mm)
            dian8 = mdb.models['myModel'].parts['Part-1'].vertices.findAt(x-1/jm,y,z-1/mm)
for x in range(1,jm+1,1):#x*jm
    for y in range(1,im+1,1):#y*10im
        for z in range(1,mm+1,1):#z*m
            x2=float(x)/jm
            y2=y*(0.4/im)
            z2=float(z)/mm
            print(x2,y2,z2)        
            dian1 = mdb.models['myModel'].parts['Part-1'].vertices.findAt(x,y,z)
            dian2 = mdb.models['myModel'].parts['Part-1'].vertices.findAt(x,y-1/im,z)
            dian3 = mdb.models['myModel'].parts['Part-1'].vertices.findAt(x-1/jm,y-1/im,z)
            dian4 = mdb.models['myModel'].parts['Part-1'].vertices.findAt(x-1/jm,y,z)
            dian5 = mdb.models['myModel'].parts['Part-1'].vertices.findAt(x,y,z-1/mm)
            dian6 = mdb.models['myModel'].parts['Part-1'].vertices.findAt(x,y-1/im,z-1/mm)
            dian7 = mdb.models['myModel'].parts['Part-1'].vertices.findAt(x-1/jm,y-1/im,z-1/mm)
            dian8 = mdb.models['myModel'].parts['Part-1'].vertices.findAt(x-1/jm,y,z-1/mm)

#step changemodel
jm=20
im=10
mm=10
for x in range(1,jm+1,1):#x*jm
    for y in range(1,im+1,1):#y*10im
        for z in range(1,mm+1,1):#z*m
            x2=float(x)/jm
            y2=y*(0.4/im)
            z2=float(z)/mm
            print(x2,y2,z2)        
            dian1 = mdb.models['myModel'].parts['Part-1'].vertices.findAt(x,y,z)
            dian2 = mdb.models['myModel'].parts['Part-1'].vertices.findAt(x,y-1/im,z)
            dian3 = mdb.models['myModel'].parts['Part-1'].vertices.findAt(x-1/jm,y-1/im,z)
            dian4 = mdb.models['myModel'].parts['Part-1'].vertices.findAt(x-1/jm,y,z)
            dian5 = mdb.models['myModel'].parts['Part-1'].vertices.findAt(x,y,z-1/mm)
            dian6 = mdb.models['myModel'].parts['Part-1'].vertices.findAt(x,y-1/im,z-1/mm)
            dian7 = mdb.models['myModel'].parts['Part-1'].vertices.findAt(x-1/jm,y-1/im,z-1/mm)
            dian8 = mdb.models['myModel'].parts['Part-1'].vertices.findAt(x-1/jm,y,z-1/mm)
            temp1 = mdb
          #  tempall = mdb.models['myModel'].steps['myStep1'].fieldOutputRequests['NT11']
            center1 =mdb.models['myModel'].rootAssmbly.parts['Part-1'].nodeSets['dian1']
            tempdian = (dian1+dian2+dian3+dian4+dian5+dian6+dian7+dian8)/8
            if tempdian>2970:
                kuan =all.cell.findAt(x-1/(2*im),y-1/(2*im),z-1/(2*im))
                mdb.models['myModel'].ModelChange(name ='deactivate',region=kuan,createStepName='Step-t+str(i*100)', activeInStep=False,includeStrain=False)
                print("active is ok")
            else:
                print("else is ok")
"""
#step2

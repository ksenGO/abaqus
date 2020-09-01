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
jm=5
im=5
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
elemType1 = mesh.ElemType(elemCode=C3D8R, elemLibrary=STANDARD, 
    kinematicSplit=AVERAGE_STRAIN, secondOrderAccuracy=OFF, 
    hourglassControl=DEFAULT, distortionControl=DEFAULT)
p1.seedPart(size=0.1, deviationFactor=0.1)
c1 = p1.cells
p1.setElementType(regions=(c1,), elemTypes=(elemType1, ))
p1.generateMesh()
print ("mesh is ok")
#material
mdb.models['myModel'].Material(name='Lv')
mdb.models['myModel'].materials['Lv'].Density(table=((2.81e-06, ), ))
mdb.models['myModel'].materials['Lv'].SpecificHeat(table=((8.54e+08, ), ))
mdb.models['myModel'].materials['Lv'].Conductivity(table=((115000, ), ))
"""
mdb.models['myModel'].materials['Lv'].Elastic(table=((210000.0,0.28),))
mdb.models['myModel'].materials['Lv'].Plastic(table=((450.0, 0.0),(480.0, 0.05),(490.0, 0.15)))
mdb.models['myModel'].materials['Lv'].Expansion(table=((1e-05,), ))
HaetTransferStep
"""
mdb.models['myModel'].HomogeneousSolidSection(name='Section-Lv',material='Lv',thickness=None)
c1 = p1.cells
region1 = regionToolset.Region(cells=c1)
print ("material is ok")
#step
moveTime=0.01
p1.SectionAssignment(region=region1,sectionName='Section-Lv',offset=0.0,offsetType=MIDDLE_SURFACE,offsetField='',thicknessAssignment=FROM_SECTION)
mdb.models['myModel'].HeatTransferStep(name='myStep1',previous='Initial',timePeriod = moveTime,maxNumInc=10000,initialInc = moveTime*0.005,minInc=moveTime*0.00001,maxInc=moveTime*0.03,deltmx=200)
#fieldoutput
fOR = mdb.models['myModel'].fieldOutputRequests['F-Output-1']
fOR.setValues(frequency=LAST_INCREMENT, variables=('HFL', 'NT'))
  

"""
FRes=mdb.models['myModel'].fieldOutputRequests
FRes[FRes.keys()[0]].setValues(numIntervals=10, variables=('NT11',))
print ("step is ok")

if NT>=2327:
    weldModel.ModelChange()
    else
"""
#load

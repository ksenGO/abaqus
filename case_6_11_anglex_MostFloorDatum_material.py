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
#feature
es = p1.edges
for j in range(1,50):
    pt1=p1.DatumPointByCoordinate(coords=(1.0*j/50,0,1))
    pt2=p1.DatumPointByCoordinate(coords=(1.0*j/50,0.4,1))
    pt3=p1.DatumPointByCoordinate(coords=(1.0*j/50,0.4,0))
    d =p1.datums
    PL1= p1.DatumPlaneByThreePoints(point1=d[pt1.id],point2=d[pt2.id],point3=d[pt3.id])
    cs = p1.cells
    CArry = [cs[0],]
    p1.PartitionCellByDatumPlane(cells=myCArry,datumPlane=d[PL1.id]) 

"""   
del CArry
del myCArry
CArray1=[]
for i in range(1,50):
    pt1=p1.DatumPointByCoordinate(coords=(0,0.4*i/50,0))
    pt2=p1.DatumPointByCoordinate(coords=(1,0.4*i/50,0))
    pt3=p1.DatumPointByCoordinate(coords=(1,0.4*i/50,1))
    d =p1.datums
    PL1= p1.DatumPlaneByThreePoints(point1=d[pt1.id],point2=d[pt2.id],point3=d[pt3.id])
    cs = p1.cells
    CArray = [cs[0],]
    CArray1.extend(CArray)
    p1.PartitionCellByDatumPlane(cells=CArray1,datumPlane=d[PL1.id])
for j in range(1,50):
    pt1=p1.DatumPointByCoordinate(coords=(1.0*j/50,0,1))
    pt2=p1.DatumPointByCoordinate(coords=(1.0*j/50,0.4,1))
    pt3=p1.DatumPointByCoordinate(coords=(1.0*j/50,0.4,0))
    d =p1.datums
    PL1= p1.DatumPlaneByThreePoints(point1=d[pt1.id],point2=d[pt2.id],point3=d[pt3.id])
    cs = p1.cells
    CArry = [cs[0],]
    myCArry.extend(CArry)
    p1.PartitionCellByDatumPlane(cells=myCArry,datumPlane=d[PL1.id]) 
"""
#mesh
elemType1 = mesh.ElemType(elemCode=C3D8R, elemLibrary=STANDARD, 
    kinematicSplit=AVERAGE_STRAIN, secondOrderAccuracy=OFF, 
    hourglassControl=DEFAULT, distortionControl=DEFAULT)
p1.seedPart(size=0.02, deviationFactor=0.1)
c1 = p1.cells
p1.setElementType(regions=(c1,), elemTypes=(elemType1, ))
p1.generateMesh()
#material
mdb.models['myModel'].Material(name='Lv')
mdb.models['myModel'].materials['Lv'].Density(table=((7.8e-09, ), ))
mdb.models['myModel'].materials['Lv'].Elastic(table=((210000.0,0.28),))
mdb.models['myModel'].materials['Lv'].Plastic(table=((450.0, 0.0),(480.0, 0.05),(490.0, 0.15)))
mdb.models['myModel'].materials['Lv'].Expansion(table=((1e-05,), ))
mdb.models['myModel'].HomogeneousSolidSection(name='Section-Lv',material='Lv',thickness=None)
c1 = p1.cells
region1 = regionToolset.Region(cells=c1)
#load

#step
p1.SectionAssignment(region=region1,sectionName='Section-Lv',offset=0.0,offsetType=MIDDLE_SURFACE,offsetField='',thicknessAssignment=FROM_SECTION)
mdb.models['myModel'].StaticStep(name='myStep1',previous='Initial',maxNumInc=1000,
    initialInc=0.1,minInc=0.001,maxInc=0.3,nlgeom = ON)
#fieldoutput
FRes=mdb.models['myModel'].fieldOutputRequests
FRes[FRes.keys()[0]].setValues(numIntervals=10, variables=('S', 'U'))

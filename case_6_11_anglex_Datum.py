from abaqus import *
from abaqusConstants import *
from caeModules import *
import material
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
es = p1.edges
pt1 =p1.DatumPointByCoordinate(coords=(0,0.1,0))
pt2 =p1.DatumPointByCoordinate(coords=(1,0.1,0))
pt3 =p1.DatumPointByCoordinate(coords=(1,0.1,1))
pt4 =p1.DatumPointByCoordinate(coords=(0,0.1,1))
d =p1.datums
PL1 = p1.DatumPlaneByThreePoints(point1=d[pt1.id],point2=d[pt2.id],point3=d[pt3.id])
cs = p1.cells
myCArry = [cs[0],]
p1.PartitionCellByDatumPlane(cells=myCArry,datumPlane=d[PL1.id])
mdb.models['myModel'].Material(name='Lv')
mdb.models['myModel'].materials['Lv'].Density(table=((7.8e-09, ), ))
mdb.models['myModel'].materials['Lv'].Elastic(table=((210000.0,0.28),))
mdb.models['myModel'].materials['Lv'].elastic
mdb.models['myModel'].materials['Lv'].Plastic(table=((450.0, 0.0),(480.0, 0.05),(490.0, 0.15)))
mdb.models['myModel'].materials['Lv'].plastic
mdb.models['myModel'].materials['Lv'].Expansion(table=((1e-05,), ))
mdb.models['myModel'].materials['Lv'].expansion
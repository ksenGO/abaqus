from abaqus import *
from abaqusConstants import *
from caeModules import *
if mdb.models.has_key('myModel'):
    m = mdb.models['myModel']
else:
    m = mdb.Model(name ='myModel')
Se = m.ConstrainedSketch(name='Extrude',sheetSize=10.0)
g,c = Se.geometry,Se.constraints
Se.setPrimaryObject(option=STANDALONE)
line1 = Se.Line(point1 = (0.0,1.0),point2 = (1.0,1.0))
line2 = Se.Line(point1 = (1.0,1.0),point2 = (1.0,0.0))
line3 = Se.Line(point1 = (1.0,0.0),point2 = (0.0,0.0))
line4 = Se.Line(point1 = (0.0,0.0),point2 =(0.0,1.0))
Se.PerpendicularConstraint(entity1 =line3,entity2 =line4)
Se.autoDimension(objectList=(line4,))
Se.unsetPrimaryObject()
p1 = mdb.models['myModel'].Part(name='Part-1',dimensionality=THREE_D,type = DEFORMABLE_BODY)
p1.BaseSolidExtrude(sketch=Se, depth=0.4)
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
mm=10
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
mdb.models['myModel'].materials['Lv'].SpecificHeat(table=((900000000000, ), ))
mdb.models['myModel'].materials['Lv'].Conductivity(table=((130, ), ))
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
for x in range(0,jm+1,1):#x*jm
    for y in range(0,im+1,1):#y*10im
        for z in range(0,mm+1,1):#z*m
            x2=float(x)/jm
            y2=y*(0.4/im)
            z2=float(z)/mm
#            print(x2,y2,z2)      
            dian1 = mdb.models['myModel'].rootAssembly.instances['Part-1-1'].vertices.findAt(((x2,y2,z2),))
#            dian2 = mdb.models['myModel'].rootAssembly.instances['Part-1-1'].vertices.findAt(((x2,y2-1/im,z2),))
#            dian3 = mdb.models['myModel'].rootAssembly.instances['Part-1-1'].vertices.findAt(((x2-1/jm,y2-1/im,z2),))
#            dian4 = mdb.models['myModel'].rootAssembly.instances['Part-1-1'].vertices.findAt(((x2-1/jm,y2,z2),))
#            dian5 = mdb.models['myModel'].rootAssembly.instances['Part-1-1'].vertices.findAt(((x2,y2,z2-1/mm),))
#            dian6 = mdb.models['myModel'].rootAssembly.instances['Part-1-1'].vertices.findAt(((x2,y2-1/im,z2-1/mm),))
#            dian7 = mdb.models['myModel'].rootAssembly.instances['Part-1-1'].vertices.findAt(((x2-1/jm,y2-1/im,z2-1/mm),))
#            dian8 = mdb.models['myModel'].rootAssembly.instances['Part-1-1'].vertices.findAt(((x2-1/jm,y2,z2-1/mm),))
            region1 = heatModel.rootAssembly.Set(vertices = dian1,name = 'Set_'+str(int(x2*100))+'_'+str(int(y2*100))+'_'+str(int(z2*100)))
#            region2 = heatModel.rootAssembly.Set(vertices = dian2,name = 'Set_'+str(int(x*100))+str(int((y-1/im)*100))+str(int(z*100)))
#            region3 = heatModel.rootAssembly.Set(vertices = dian3,name = 'Set_'+str(int((x-1/jm)*100))+str(int((y-1/im)*100))+str(int(z*100)))
#            region4 = heatModel.rootAssembly.Set(vertices = dian4,name = 'Set_'+str(int((x-1/jm)*100))+str(int(y*100))+str(int(z*100)))
#            region5 = heatModel.rootAssembly.Set(vertices = dian5,name = 'Set_'+str(int(x*100))+str(int(y*100))+str(int((z-1/mm)*100)))
#            region6 = heatModel.rootAssembly.Set(vertices = dian6,name = 'Set_'+str(int(x*100))+str(int((y-1/im)*100))+str(int((z-1/mm)*100)))
#            region7 = heatModel.rootAssembly.Set(vertices = dian7,name = 'Set_'+str(int((x-1/jm)*100))+str(int((y-1/im)*100))+str(int((z-1/mm)*100)))
#            region8 = heatModel.rootAssembly.Set(vertices = dian8,name = 'Set_'+str(int((x-1/jm)*100))+str(int(y*100))+str(int((z-1/mm)*100)))         
#load-1
import load 
ipart = heatModel.rootAssembly.instances['Part-1-1']
allsetName = 'Set-all'
allset = heatModel.rootAssembly.Set(cells= ipart.cells,name = allsetName)
heatModel.Temperature(name='Predefined',createStepName = 'Initial',region = allset,magnitudes = 20)
s1 = a.instances['Part-1-1'].faces
side1Faces1 = s1.findAt(((0.45,0.0,0.45),),((0.35,0.0,0.35),),((0.45,0.0,0.35),))
region = a.Surface(side1Faces= side1Faces1,name ='Surf-1')
mdb.models['myModel'].SurfaceHeatFlux(name = 'heatload', createStepName = 'Heating Step', region=region,magnitude =400000)
heatModel.setValues(absoluteZero = -273.15,stefanBoltzmann=5.67E-8)
import job
#Creat the job
mdb.Job(name ='HeatTransferJob3',model ='myModel',type = ANALYSIS)
mdb.jobs['HeatTransferJob3'].submit(consistencyChecking=OFF)
mdb.jobs['HeatTransferJob3'].waitForCompletion()
print ("step1 is ok")
#Create the step-2
import step
heatModel = mdb.models['myModel']
moveTime=10
heatModel.HeatTransferStep(name='Heating Step2', previous='Heating Step', 
        timePeriod=moveTime, maxNumInc=10000, initialInc=moveTime*0.005, 
        minInc=moveTime*1e-8, maxInc=moveTime*0.03, deltmx=200.0)
#extract temp
from odbAccess import*
from abaqusConstants import*
import os
import sys
from textRepr import*
myodb = openOdb(path=r'D:\abaqus\00\HeatTransferJob3.odb')
lastFrame = myodb.steps['Heating Step'].frames[-1]
temp = lastFrame.fieldOutputs['NT11']
setx = myodb.rootAssembly.nodeSets['SET_500100400']
temp1=temp.getSubset(region=setx ).values[0].data
#modelchangge

if temp1>20:
    print('yes')
else:
    print('no')
prettyPrint(temp1)

mdb.models['myModel'].FieldOutputRequest(name ='F-Output-step_2',numIntervals=1,createStepName='Heating Step2',variables=('NT','HFL'))
#load-2
import load 
s1 = a.instances['Part-1-1'].faces
side1Faces1 = s1.findAt(((0.45,0.0,0.45),),((0.35,0.0,0.35),),((0.45,0.0,0.35),))
region = a.Surface(side1Faces= side1Faces1,name ='Surf-1')
mdb.models['myModel'].SurfaceHeatFlux(name = 'heatload2', createStepName = 'Heating Step2', region=region,magnitude = 300000)
heatModel.setValues(absoluteZero = -273.15,stefanBoltzmann=5.67E-8)
print ("step2 is ok")       
#Creat the job
mdb.Job(name ='HeatTransferJob2',model ='myModel',type = ANALYSIS)
mdb.jobs['HeatTransferJob2'].submit(consistencyChecking=OFF)
mdb.jobs['HeatTransferJob2'].waitForCompletion()
'''
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
           #odbs['HeatTransferJob3.odb'].steps['Heating Step'].frames[-1].FieldOutputs
            region1 = heatModel.rootAssembly.Set(vertices = dian1,name = 'Set_+str(x)_+str(y)_+str(z)')

            center1 =myodb.rootAssembly.instances['PART-1-1'].nodeSets['region1']
            temp1=temp.getSubset(region=dian1)
            temp2=temp.getSubset(region=dian2)
            temp3=temp.getSubset(region=dian3)
            temp4=temp.getSubset(region=dian4)
            temp5=temp.getSubset(region=dian5)
            temp6=temp.getSubset(region=dian6)
            temp7=temp.getSubset(region=dian7)
            temp8=temp.getSubset(region=dian8)
            temp0=(temp1+temp2+temp3+temp4+temp5+temp6+temp7+temp8)
'''
"""
#extract temp
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
'''
            #center1 =myodb.rootAssembly.instances['PART-1-1'].nodeSets['region1']
            temp1=temp.getSubset(region=region1)
            temp2=temp.getSubset(region=region2)
            temp3=temp.getSubset(region=region3)
            temp4=temp.getSubset(region=region4)
            temp5=temp.getSubset(region=region5)
            temp6=temp.getSubset(region=region6)
            temp7=temp.getSubset(region=region7)
            temp8=temp.getSubset(region=region8)
            temp0=(temp1+temp2+temp3+temp4+temp5+temp6+temp7+temp8)
'''
'''    
ta1 = mdb.models['myModel'].rootAssembly
tv1 = ta1.instances['Part-1-1'].vertices
x=1.0
y=0
z=1
tverts1 =tv1.findAt(((x,y,z),))
ttregion = ta1.Set( vertices= tverts1,name='set'+str(int(x*10))+str(y)+str(z)) 
'''
#f=odb.steps['Heating Step'].frames[-1].fieldOutputs['NT11']
#D=f.getSubset(Position=SET_10001001000)
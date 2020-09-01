from abaqus import *
from abaqusConstants import *
from caeModules import *
import material
import re, platform
def buildFor(Q=3000.0,factor1=1.0,source_a1=1.9,source_b1=3.2,source_c1=2.8,source_a2=1.9, weldingV=4.0,source_x0=0.0,source_y0=4.0,source_z0=0.0):
        
    tempName='dual_ellipse_plate.template'
    forName='dual_ellipse_Welding.for'
    f1=open(tempName,'r')
    f2=open(forName,'w')

    for line in f1.readlines():
        ss=line.strip()
        ss0=re.split('=',ss)
        ss1=re.split('=',line)
        if ss0[0]=='q':
            sstemp=ss1[0]+'='+str(Q)+'\n'
            f2.writelines(sstemp)
        elif ss0[0]=='f1':
            sstemp=ss1[0]+'='+str(factor1)+'\n'
            f2.writelines(sstemp)
        elif ss0[0]=='a':
            sstemp=ss1[0]+'='+str(source_a1)+'\n'
            f2.writelines(sstemp)
        elif ss0[0]=='b':
            sstemp=ss1[0]+'='+str(source_b1)+'\n'
            f2.writelines(sstemp)
        elif ss0[0]=='c':
            sstemp=ss1[0]+'='+str(source_c1)+'\n'
            f2.writelines(sstemp)
        elif ss0[0]=='aa':
            sstemp=ss1[0]+'='+str(source_a2)+'\n'
            f2.writelines(sstemp)
        elif ss0[0]=='x0':
            sstemp=ss1[0]+'='+str(source_x0)+'\n'
            f2.writelines(sstemp)
        elif ss0[0]=='y0':
            sstemp=ss1[0]+'='+str(source_y0)+'\n'
            f2.writelines(sstemp)
        elif ss0[0]=='z0':
            sstemp=ss1[0]+'='+str(source_z0)+'\n'
            f2.writelines(sstemp)
        elif ss0[0]=='v':
            sstemp=ss1[0]+'='+str(weldingV)+'\n'
            f2.writelines(sstemp)
        else:
            f2.writelines(line)
    f1.close()
    f2.close()

    return forName
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
#feature
es = p1.edges
jm=10
im=10
mm=10
model_change_i=1
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
#mesh#mesh
elemType1 = mesh.ElemType(elemCode=DC3D8, elemLibrary=STANDARD, 
    kinematicSplit=AVERAGE_STRAIN, secondOrderAccuracy=OFF, 
    hourglassControl=DEFAULT, distortionControl=DEFAULT)
p1.seedPart(size=0.1, deviationFactor=0.1)
c1 = p1.cells
p1.setElementType(regions=(c1,), elemTypes=(elemType1, ))
p1.generateMesh()
#material
#material
mdb.models['myModel'].Material(name='Lv')
mdb.models['myModel'].materials['Lv'].Density(table=((3.5e-06, ), ))
mdb.models['myModel'].materials['Lv'].SpecificHeat(table=((1.33e+09, ), ))
mdb.models['myModel'].materials['Lv'].Conductivity(table=((5500, ), ))
mdb.models['myModel'].HomogeneousSolidSection(name='Section-Lv',material='Lv',thickness=None)
c1 = p1.cells
region1 = regionToolset.Region(cells=c1)
p1.SectionAssignment(region = region1,sectionName = 'Section-Lv',offset =0.0,offsetType = MIDDLE_SURFACE,offsetField='',thicknessAssignment= FROM_SECTION)
print ("material is ok")
#Assembly
a = mdb.models['myModel'].rootAssembly
p11 = a.Instance(name = 'Part-1-1',part = p1,dependent = ON)
heatModel = mdb.models['myModel']
for x in range(0,jm+1,1):#x*jm
    for y in range(0,im+1,1):#y*10im
        for z in range(0,mm+1,1):#z*m
            x2=float(x)/jm
            y2=y*(0.4/im)
            z2=float(z)/mm
            #print(x2,y2,z2)      
            dian1 = mdb.models['myModel'].rootAssembly.instances['Part-1-1'].vertices.findAt(((x2,y2,z2),))
            region1 = heatModel.rootAssembly.Set(vertices = dian1,name = 'Set_'+str(int(x2*100))+'_'+str(int(y2*100))+'_'+str(int(z2*100)))
ipart = heatModel.rootAssembly.instances['Part-1-1']
allsetName = 'Set-all'
allset = heatModel.rootAssembly.Set(cells= ipart.cells,name = allsetName)
heatModel.Temperature(name='Predefined',createStepName = 'Initial',region = allset,magnitudes = 20)
#heatstepbysetp
totol_heat_stepnum =5
each_heat_steptime = 0.0001   #s#changge 
downnum =0
preFoutput ='F-Output-1'
import step
import load
for stepnum_i in range(1,totol_heat_stepnum):
    stepNameheat = 'step_'+str(stepnum_i)
    FoutputName = 'F-Output-step'+str(stepnum_i)
    heatLoad ='load-'+str(stepnum_i)
    if stepnum_i == 1:
        heatModel.HeatTransferStep(name=stepNameheat, previous='Initial', 
            timePeriod=each_heat_steptime, maxNumInc=10000, initialInc=each_heat_steptime*0.005, 
            minInc=each_heat_steptime*1e-8, maxInc=each_heat_steptime*0.03, deltmx=200.0)  
        print(1)

    else:
        print(2,stepNameheat)
        heatModel.HeatTransferStep( minInc=each_heat_steptime*1e-8, maxInc=each_heat_steptime*0.03, deltmx=200.0,
            timePeriod=each_heat_steptime, maxNumInc=10000, initialInc=each_heat_steptime*0.005, 
            name=stepNameheat, previous=preStep)
    preStep= 'step_'+str(stepnum_i)
    #extract temp and model change
    if stepnum_i == 1:
        print(stepNameheat)
    else:
        from odbAccess import*
        from abaqusConstants import*
        import os
        import sys
        from textRepr import*
        print('extractemp'+str(stepnum_i-1)+'.odb')
        myodb = openOdb(path=r'D:\abaqus\00\HeatTransferJob_'+str(stepnum_i-1)+'.odb')
        laststepNameheat = 'step_'+str(stepnum_i-1)
        lastFrame = myodb.steps[laststepNameheat].frames[-1]
        temp = lastFrame.fieldOutputs['NT11']
        
        print('extract temp and model change_'+laststepNameheat)
        for x in range(1,jm+1,1):#x*jm
            for z in range(1,mm+1,1):#z*m
                stepNameheat_downnum_x_z_i = 0
                for y in range(1,im+1,1):#y*10im
                    x2=float(x)/jm
                    y2=y*(0.4/im)
                    z2=float(z)/mm
                    #setx = myodb.rootAssembly.nodeSets['SET_40_0_40']
                    #temp=temp.getSubset(region=setx ).values[0].data
                   # print(x2,y2,z2)
                    setx1 = myodb.rootAssembly.nodeSets['SET_'+str(int(x2*100))+'_'+str(int(y2*100))+'_'+str(int(z2*100))]
                    setx2 = myodb.rootAssembly.nodeSets['SET_'+str(int(x2*100))+'_'+str(int(y2*100-40/im))+'_'+str(int(z2*100))]
                    setx3 = myodb.rootAssembly.nodeSets['SET_'+str(int(x2*100-100/jm))+'_'+str(int(y2*100-40/im))+'_'+str(int(z2*100))]
                    setx4 = myodb.rootAssembly.nodeSets['SET_'+str(int(x2*100-100/jm))+'_'+str(int(y2*100))+'_'+str(int(z2*100))]
                    setx5 = myodb.rootAssembly.nodeSets['SET_'+str(int(x2*100))+'_'+str(int(y2*100))+'_'+str(int(z2*100-100/mm))]
                    setx6 = myodb.rootAssembly.nodeSets['SET_'+str(int(x2*100))+'_'+str(int(y2*100-40/im))+'_'+str(int(z2*100-100/mm))]
                    setx7 = myodb.rootAssembly.nodeSets['SET_'+str(int(x2*100-100/jm))+'_'+str(int(y2*100-40/im))+'_'+str(int(z2*100-100/mm))]
                    setx8 = myodb.rootAssembly.nodeSets['SET_'+str(int(x2*100-100/jm))+'_'+str(int(y2*100))+'_'+str(int(z2*100-100/mm))]
                    temp1=temp.getSubset(region=setx1).values[0].data
                    temp2=temp.getSubset(region=setx2).values[0].data
                    temp3=temp.getSubset(region=setx3).values[0].data
                    temp4=temp.getSubset(region=setx4).values[0].data
                    temp5=temp.getSubset(region=setx5).values[0].data
                    temp6=temp.getSubset(region=setx6).values[0].data
                    temp7=temp.getSubset(region=setx7).values[0].data
                    temp8=temp.getSubset(region=setx8).values[0].data
                    temp9 = (temp1+temp2+temp3+temp4+temp5+temp6+temp7+temp8)/8
                    #print(temp1,temp2,temp3,temp4,temp5,temp6,temp7,temp8,temp9)
                    if temp9>1000:
                        modelchangename ='modelchangename_'+str(model_change_i)
                        modelchange = 'modelchange_'+str(model_change_i)
                        modelchangepoint1 = mdb.models['myModel'].rootAssembly.instances['Part-1-1'].cells.findAt(((x2-(1.0/jm/2),y2-(0.4/im/2),z2-(1.0/im/2)),))
                        modelchange= heatModel.rootAssembly.Set(cells = modelchangepoint1,name = modelchangename)
                        weldModel = mdb.models['myModel']
                        weldModel.ModelChange(name=modelchangename,createStepName=stepNameheat,region = modelchange,activeInStep=False,includeStrain = False)
                        model_change_i=model_change_i+1
                        stepNameheat_downnum_x_z_i = stepNameheat_downnum_x_z_i + 1
                        downnum =stepNameheat_downnum_x_z_i+downnum
                if stepNameheat_downnum_x_z_i == 0:
                    pass
                else:
                    print(x2,downnum ,z2)
    heatModel.FieldOutputRequest(name=FoutputName,numIntervals=1,createStepName=stepNameheat, variables=('HFL', 'NT'))
    print(FoutputName)  
    mdb.models['myModel'].BodyHeatFlux(name = heatLoad, createStepName = stepNameheat, region=allset,distributionType = USER_DEFINED)
    heatModel.setValues(absoluteZero = -273.15,stefanBoltzmann=5.67E-8)
    import job
    weldingV=1000#mm/s
    s_Q=2000e6#mW
    s_a1=0.25#mm
    s_b1=0.15#mm
    s_c1=0.2#mm
    s_a2=0.25#mm
    s_x0=0.0#mm
    s_y0=0.5#mm
    s_z0=0.5#mm
    dfluxName=buildFor(Q=s_Q,factor1=1.0,source_a1=s_a1,source_b1=s_b1,
    source_c1=s_c1,source_a2=s_a2, weldingV=weldingV,
    source_x0=s_x0,source_y0=s_y0,source_z0=s_z0)
    print('extractemp'+str(stepnum_i-1)+'.odb')

    jobName = 'HeatTransferJob_'+str(stepnum_i)
    mdb.Job(name =jobName,model ='myModel',type = ANALYSIS, userSubroutine=dfluxName)
    mdb.jobs[jobName].submit(consistencyChecking=OFF)
    mdb.jobs[jobName].waitForCompletion()
    stepOk = 'step-'+str(stepnum_i)+'is ok'
    print (stepOk)

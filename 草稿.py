for m in range(2,50): 
    print(("pt"+str(m)+str(1)))
    print type(Feature(("pt"+str(m)+str(1))))
 

 for m in range(1,50):
    d =p1.datums
    ("PL"+str(m))= p1.DatumPlaneByThreePoints(point1=d[("pt"+str(m)+str(1)).id],point2=d[("pt"+str(m)+str(2).id],point3=d[("pt"+str(m)+str(3)).id])
    cs = p1.cells
    myCArry = [cs[50],]
    p1.PartitionCellByDatumPlane(cells=myCArry,datumPlane=d[("PL"+str(i)).id])


           d =p1.datums
        ("PL"+str(i))= p1.DatumPlaneByThreePoints(point1=d[("pt"+str(i)+str(1)).id],point2=d[("pt"+str(i)+str(2).id],point3=d[("pt"+str(i)+str(3)).id])
        cs = p1.cells
        myCArry = [cs[50],]
        p1.PartitionCellByDatumPlane(cells=myCArry,datumPlane=d[("PL"+str(i)).id])
i =50
m =i/50
print(m)
    d =p1.datums
    ("PL"+str(i))= p1.DatumPlaneByThreePoints(point1=d[("pt"+str(i)+str(1)).id],point2=d[("pt"+str(i)+str(2).id],point3=d[("pt"+str(i)+str(3)).id])
    cs = p1.cells
    myCArry = [cs[50],]
    p1.PartitionCellByDatumPlane(cells=myCArry,datumPlane=d[("PL"+str(i)).id])

i = 3
print (0.4*i/50)
d =p1.datums
PL1= p1.DatumPlaneByThreePoints(point1=d[pt1.id],point2=d[pt2.id],point3=d[pt3.id])
cs = p1.cells
myCArry = [cs[55],]
p1.PartitionCellByDatumPlane(cells=myCArry,datumPlane=d[("PL"+str(i)).id])
for i in range(1,2):
    ("pt"+str(i)+str(1))=p1.DatumPointByCoordinate(coords=(0,0.4*i/50,0))
    ("pt"+str(i)+str(2))=p1.DatumPointByCoordinate(coords=(1,0.4*i/50,0))
    ("pt"+str(i)+str(3))=p1.DatumPointByCoordinate(coords=(1,0.4*i/50,1))
    print type(("pt"+str(m)+str(1)))
("pt"+str(2)+str(1))=p1.DatumPointByCoordinate(coords=(0,0.4*50,0))
print type(("pt"+str(2)+str(1)))

    d =p1.datums
    PL1= p1.DatumPlaneByThreePoints(point1=d[pt1.id],point2=d[pt2.id],point3=d[pt3.id])
    cs = p1.cells
    myCArry = [cs[0],cs[1],cs[2]]
    p1.PartitionCellByDatumPlane(cells=myCArry,datumPlane=d[PL1.id])

    cs = p1.cells
    CArry = [cs[0],]
    myCArry.extend(CArry)
    p1.PartitionCellByDatumPlane(cells=myCArry,datumPlane=d[PL1.id])

    cs = p1.cells
    CArry = [cs[0],]
    myCArry.extend(CArry)
    p1.PartitionCellByDatumPlane(cells=myCArry,datumPlane=d[PL1.id]
    cs = p1.cells
    myCArray = [cs[0],]
    myCArray.extend(myCArray)
    p1.PartitionCellByDatumPlane(cells=myCArray,datumPlane=d[PL1.id])
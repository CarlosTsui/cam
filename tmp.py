import math
pi=3.14159265358979723846
ags=[0 for x in range(0,20)]        #angle_sin
agc=[0 for x in range(0,20)]        #angle_cos
agh=[0 for x in range(0,20)]
angle=22.5
for i in range(1,9):
    agh[i]=2*pi*angle/360
    ags[i]=math.sin(agh[i])
    agc[i]=math.cos(agh[i])
    print(i,angle,agh[i],agc[i])
    angle+=45;

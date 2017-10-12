from mpl_toolkits.mplot3d import Axes3D
import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm

#Monopole function
def monopolepowerdB(freq, ratio, angle):
    c = 299792458.0 #m/s
    lambd = c/freq
    k = 2*math.pi/lambd
    h = ratio*lambd
    if angle == 0:
        return -float('inf')
    else:
        return 10*math.log10(((math.cos(k*h*math.cos(angle))-math.cos(k*h))/math.sin(angle))**2);

#ADSb helix function
def helixpowerdB(angle):
    return -2e-8*(angle**5)+1e-6*(angle**4)+.0002*(angle**3)-0.0202*(angle**2)+0.2044*angle+8.6413;

def helixpower(angle): 
    if angle > 50:
        return 1e-1
    return (3e-10)*(angle**6)-(5e-8)*(angle**5)+(8e-7)*(angle**4)+.0003*(angle**3)-0.0162*(angle**2)+0.0595*angle+7.4131;

def radarpowerdB(angle):
    halfangle = 12.5
    gain = 30
    if angle < 2*halfangle:
        return gain - angle/halfangle*3
    return gain - 6 - (angle-2*halfangle)/halfangle*12;

def CSLGaindBi(Gain, angle):
    #
    #SSG_INVESTIGATION_PORT2_ANG10.txt


    f = open('SSG_INVESTIGATION_PORT2_ANG10_FULL_RANGE_CORRECTION.txt', 'r')
    x = f.readlines()
    x_num = [float(x1) for x1 in x]

    angle_DEG = int(angle) + 180
    if angle_DEG < 360:
        return Gain[angle_DEG]
    return np.min(Gain);


f = open('SSG_INVESTIGATION_PORT2_ANG10_FULL_RANGE_CORRECTION.txt', 'r')
x = f.readlines()
x_num = [float(x1) for x1 in x]
f.close()

f_1 = open('SSG_INVESTIGATION_PORT2_ANG10_FULL_RANGE_CORRECTION.txt', 'r')
x_1 = f_1.readlines()
x_num_1 = [float(x2) for x2 in x_1]
f_1.close()

Max_Coverage = 3000

#SatelliteAntGain = 0#dBi
CableLossdB = 0 # was -3
ChannelLossdB = 0 # Fading, interference and polarization was - 3 dB
DataRate = 60 #dB/s @ 1Mbps
Noise = -202.7 # dBW/Hz
# Tx_Power = 4 W
Tx_Power_dBW = 6
#Bandwidth_kHz =
#ref_Bandwidth_kHz =

h = 750 #km
r = 6371.0 #km
flightangle = 0# deg
earthDist = np.array(range(-Max_Coverage, 0, 1))
earthAng = earthDist / r
slantRange = [math.sqrt((r+h)**2+r**2-2*(r+h)*r*math.cos(num)) for num in earthAng]
earthElev = [math.acos((r**2+num**2-(r+h)**2)/(2*num*r)) for num in slantRange]


c = 299792458.0 # m/s
f = 9.41e9 # Hz
Pathloss = [(c/(4*math.pi*num*1000*f))**2 for num in slantRange]
PathlossdB = [10*math.log10(num) for num in Pathloss]


CSLgain_PORT1 = [CSLGaindBi(x_num , abs((math.pi-num-num2)*180.0/math.pi-flightangle )) for num,num2 in zip(earthElev,earthAng)]
Half_Cone_Angle = [abs((math.pi-num-num2)*180.0/math.pi-flightangle) for num,num2 in zip(earthElev,earthAng)]
CSLgain_PORT2 = [CSLGaindBi(x_num_1 , abs((math.pi-num-num2)*180.0/math.pi-flightangle )) for num,num2 in zip(earthElev,earthAng)]

#plt.plot(-earthDist,CSLgain_PORT1)
#plt.plot(slantRange,CSLgain_PORT1)
plt.plot(Half_Cone_Angle,slantRange)

Spacer = '        '
Column_description = 'Elevation Angle in degrees'+Spacer+'Range in kms'
File_name_target = 'ITU_Verficiation.txt'
f_target = open(File_name_target, 'w')
f_target.write(Column_description)

for i in range(1, 3000):
    Text_Line = str(Half_Cone_Angle[i]) + Spacer + str(slantRange[i])+ '\n'
    f_target.write(Text_Line)

#plt.plot(earthDist,CSLgain_PORT2)
#plt.plot(slantRange,CSLgain_PORT2)
#plt.plot(earthDist,alphaangle)
plt.ylim([-1000, 5000])
plt.xlim([0, 90])
plt.ylabel('half-cone angle')
plt.xlabel('Range Earth to sat at orbit '+str(h)+' km inclination '+str(flightangle)+' degrees')
plt.grid(b=True)

for i in range(0, len(Half_Cone_Angle)):
    if ( 44.95 < Half_Cone_Angle[i] < 45.05 ):
        stash_i = i;

print(slantRange[stash_i])
print(CSLgain_PORT1[stash_i])

#plt.subplot(413)
#plt.plot(earthDist,radarGain)
##[num*180/math.pi-90.0 for num in earthElev])
#plt.ylim([-20, 35])
#plt.xlim([0, 2550])
##plt.ylabel('Radar gain towards satellite [dB]')
##plt.xlabel('Surface distance for orbit altitude of '+str(h)+' km')
#plt.grid(b=True)

#plt.subplot(414)
#trueMargindA = [monopolepowerdB(1090e6,2.0/8.0,abs(math.pi-num)) + num2 + num3 for num,num2,num3 in zip(earthElev,LinkMarginA,ADSbgain)]
#trueMargindA = [-10+num*0 + num2 + num3 for num,num2,num3 in zip(earthElev,LinkMargin,ADSbgain)]

pulseDuration = 0.6e-6
bandWidth = 15e6
noiseTemp = 500
bolzman = -228.5991678 # dBW/(K*Hz)
noiseFloor = 0 #bolzman + 30 + 10*math.log10(noiseTemp) + 10*math.log10(bandWidth)
#print noiseFloor

#receivedPower = [(num1 + num2 + num3) - noiseFloor for num1,num2,num3 in zip(LinkMargin,radarGain,ESMgain)]


##plt.plot(earthDist,receivedPower)
#plt.ylim([-110, -70])
#plt.xlim([0, 2550])
#plt.ylabel('Signal strength [dBm]')
#plt.xlabel('Surface distance for orbit altitude of '+str(h)+' km')
#plt.grid(b=True)

#plt.savefig('AIS_ClassA_'+str(h)+'alt.pdf', bbox_inches='tight')
plt.show()

#p = np.linspace(0,2*np.pi,60)
#R,P = np.meshgrid(earthDist,p)
#X,Y = R*np.cos(P),R*np.sin(P)

#Z = map(lambda x: float('NaN') if x < 10 else x, trueMargindB)
#fig = plt.figure()
#ax = fig.add_subplot(111, projection='3d')
#ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.YlGnBu_r)
#ax.set_zlim3d(0, 30)
#plt.show()

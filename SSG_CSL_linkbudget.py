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

def terminalpowerdB(angle):
    halfangle = 12.5
    gain = 30
    if angle < 2*halfangle:
        return gain - angle/halfangle*3
    return gain - 6 - (angle-2*halfangle)/halfangle*12;

def CSLpowerdB(angle):
    halfangle = 36
    gain = 8
    if angle < 2*halfangle:
        return gain - angle/halfangle*3
    return gain - 6 - (angle-2*halfangle)/halfangle*12;

CSLPowerdBm = 33 # verified
#SatelliteAntGain = 0#dBi
CableLossdB = -2 # was -3
ChannelLossdB = 0 # Fading, interference and polarization changed from -3
DataRate = -7 #dB/s @ 200 kbps
Noise = -202.7 # dBW/Hz
SSGTerminALAntGaindB = 8 # added by Claude afterward for verification

h = 750.0 #km
r = 6371.0 #km
flightangle = 0.0 # deg
earthDist = np.array(range(0, 10000,10 ))
earthAng = earthDist / r
slantRange = [math.sqrt((r+h)**2+r**2-2*(r+h)*r*math.cos(num)) for num in earthAng]
earthElev = [math.acos((r**2+num**2-(r+h)**2)/(2*num*r)) for num in slantRange]


c = 299792458.0 # m/s
f = 2.2e9 # Hz
Pathloss = [(c/(4*math.pi*num*1000*f))**2 for num in slantRange]
PathlossdB = [10*math.log10(num) for num in Pathloss]

LinkMargin = [CSLPowerdBm+CableLossdB+ChannelLossdB+SSGTerminALAntGaindB+num for num in PathlossdB] # No datarate and noise
# What is called LinkMargin is Pout_ant = PFD + G + (Lambda2/4pi) all in dB


plt.subplot(412)
AngleDeg = [abs((math.pi-num-num2)*180.0/math.pi-flightangle ) for num,num2 in zip(earthElev,earthAng)]
CSLgain = [CSLpowerdB(abs((math.pi-num-num2)*180.0/math.pi-flightangle )) for num,num2 in zip(earthElev,earthAng)]

alphaangle = [90-((math.pi-num-num2)*180.0/math.pi) for num,num2 in zip(earthElev,earthAng)]
terminalGain = [terminalpowerdB(num*180/math.pi-90.0) for num in earthElev]
plt.plot(earthDist,CSLgain)
#plt.plot(earthDist,alphaangle)
plt.ylim([-40, 20])
plt.xlim([0, 2550])
plt.ylabel('CSL antenna gain [dB]')
#plt.xlabel('Surface distance for orbit altitude of '+str(h)+' km')
plt.grid(b=True)


plt.subplot(413)
plt.plot(AngleDeg,CSLgain)
#plt.plot(earthDist,alphaangle)
plt.ylim([-40, 20])
plt.xlim([0, 50])
plt.ylabel('CSL antenna gain [dB]')
#plt.xlabel('Surface distance for orbit altitude of '+str(h)+' km')
plt.grid(b=True)
#plt.plot(earthDist,terminalGain)
##[num*180/math.pi-90.0 for num in earthElev])
#plt.ylim([-20, 35])
#plt.xlim([0, 2550])
##plt.ylabel('terminal gain towards satellite [dB]')
##plt.xlabel('Surface distance for orbit altitude of '+str(h)+' km')
#plt.grid(b=True)

plt.subplot(414)
#trueMargindA = [monopolepowerdB(1090e6,2.0/8.0,abs(math.pi-num)) + num2 + num3 for num,num2,num3 in zip(earthElev,LinkMarginA,ADSbgain)]
#trueMargindA = [-10+num*0 + num2 + num3 for num,num2,num3 in zip(earthElev,LinkMargin,ADSbgain)]

pulseDuration = 0.6e-6
bandWidth = 15e6
noiseTemp = 500
bolzman = -228.5991678 # dBW/(K*Hz)
noiseFloor = 0 #bolzman + 30 + 10*math.log10(noiseTemp) + 10*math.log10(bandWidth)
#print noiseFloor

receivedPower = [(num1 + num2 + num3) - noiseFloor for num1,num2,num3 in zip(LinkMargin,terminalGain,CSLgain)]



## start for uncom
#p = np.linspace(0,2*np.pi,60)
#R,P = np.meshgrid(earthDist,p)
#X,Y = R*np.cos(P),R*np.sin(P)

#Z = map(lambda x: float('NaN') if x < 10 else x, trueMargindB)
#fig = plt.figure()
#ax = fig.add_subplot(111, projection='3d')
#ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.YlGnBu_r)
#ax.set_zlim3d(0, 30)
plt.show()

from mpl_toolkits.mplot3d import Axes3D
import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
from matplotlib.pyplot import *
import matplotlib.markers
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from numpy import loadtxt

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

def ReadGainFile(file_name):
#    f = open(file_name, 'r')
#    x = f.readlines()
    Gain = np.arange(0,360,1)*0.1
    lines = tuple(open(file_name, 'r'))
    for i in range(0,360):
        text = lines[i+2].split('         ')
        if len(text) == 8:
            Gain_stash = float(text[2]);
        if len(text) == 7:
            Gain_stash = float(text[1]);
        Gain[i] = Gain_stash
    return Gain;

def CSLGaindBi(Gain, angle):

    angle_DEG = int(angle)
    if angle_DEG < 360:
        return Gain[angle_DEG];
#    return np.min(Gain);

def dTPUT(Gain_Tx_dBi, Gain_Rx_dBi, distance_Km):
    # Constant
    Light_Velocity_ms = 300000000
    Boltzmann = -228.6

    # LINK BUDGET INPUT
    Carrier_Frequency_MHz = 2200
    Carrier_Wavelength = Light_Velocity_ms / (Carrier_Frequency_MHz * 1000000)
    Distance_Tx_Rx_km = distance_Km
    Typical_symbol_rate_kb_s = 500
    Receive_channel_bandwidth_kHz = Typical_symbol_rate_kb_s * 0.675 * 2
    Usefull_bitrate = 500
    Coding_gain = 4.8
    Required_Eb_No = 8.4
    Receiver_implementation_loss = 0.5

    # Transmitter
    Tx_Antenna_Gain_dBi = Gain_Tx_dBi

    Tx_RF_Power_W = 2
    Tx_Losses_dB = 0.2
    Tx_EIRP_dBW = 10 * np.log10(Tx_RF_Power_W) + Tx_Antenna_Gain_dBi - Tx_Losses_dB
    Additional_loss_dB = 1
    Propagation_loss_dB = -10 * np.log10((Carrier_Wavelength / 4 / 3.1415926 / Distance_Tx_Rx_km / 1000) * (
    Carrier_Wavelength / 4 / 3.1415926 / Distance_Tx_Rx_km / 1000)) + Additional_loss_dB

    # Receiver
    Rx_Antenna_Gain_dBi = Gain_Rx_dBi
    Antenna_Noise_Temperature_K = 75
    Sat_Noise_and_interference_K = 200
    Antenna_Signal_Level_dBm = Tx_EIRP_dBW + 30 - Propagation_loss_dB + Rx_Antenna_Gain_dBi
    Receiver_Noise_Figure_dB = 3.2
    System_Noise_Temperature = Antenna_Noise_Temperature_K + Sat_Noise_and_interference_K + 280 * (
    np.power(10, (Receiver_Noise_Figure_dB / 10)) - 1)
    System_Noise_Temperature_dBK = 10 * np.log10(System_Noise_Temperature)
    Rx_GT = Rx_Antenna_Gain_dBi - System_Noise_Temperature_dBK
    Final_C_No = Tx_EIRP_dBW + Rx_GT - Propagation_loss_dB - Boltzmann
    C_N0_required = Required_Eb_No + 10 * np.log10(
        Receive_channel_bandwidth_kHz * 1000) - Coding_gain + Receiver_implementation_loss
    Margin_A_B = Final_C_No - C_N0_required
    Noise_density_received_dBW_per_Hz = System_Noise_Temperature_dBK + Boltzmann

    SNR = Antenna_Signal_Level_dBm - Noise_density_received_dBW_per_Hz - 10 * np.log10(
        Receive_channel_bandwidth_kHz * 1e3) - 30
    dTPUT = 10 ** ((Margin_A_B) / 10) * Usefull_bitrate
    return(dTPUT)

File_name = ["" for x in range(3)]
File_name[1] = 'Port12_2062_90.txt'
File_name[2] = 'Port12_2062_80.txt'
File_name_target = 'Gain_dTPUT'
Column_description = 'Distance in kms         Angle_of_Arrival_in_deg         Gain_in_Tx_dBi         Gain_in_Rx_dBi         dTPUT_kb_per_second\n'
Spacer = '         '

Gain_Tx = ReadGainFile(File_name[1])
Gain_Rx = ReadGainFile(File_name[2])

f_target = open(File_name_target, 'w')
f_target.write(Column_description)


# Geometrical constants
Max_Coverage = 3000
h = 750.0  # km
r = 6371.0  # km
flightangle = 15 # deg
c = 299792458.0  # m/s
f = 9.41e9  # Hz
Angle_step = 10 #deg
Max_Distance_Km = 1000
Max_Angle_InPlane_Deg = 90

Tx_Gain = np.max(Gain_Tx)

for distance in range(1, Max_Distance_Km+1):
    for angle_to_inplane_deg in range (0, Max_Angle_InPlane_Deg):
        dTPUT_scalar = dTPUT(Tx_Gain, Gain_Rx[angle_to_inplane_deg], distance)
        Text_Line = str(distance) + Spacer + str(angle_to_inplane_deg) + Spacer + str(Tx_Gain)+ Spacer + str(Gain_Rx[angle_to_inplane_deg])+ Spacer + str(dTPUT_scalar) + '\n'
        print(dTPUT_scalar)
        f_target.write(Text_Line)


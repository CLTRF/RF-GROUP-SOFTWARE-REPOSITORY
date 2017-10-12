import visa
import time
import datetime

# initializations for 1
f = open('FM_SCAN_CHANNELA', 'w')
f.write('GOM4-X PROJECT TEST3ON BOARD FM Rx3 LidOn Antenna On ter\n')
f.write('LOSS TO IF CABLE: Not CALibrated to be done dB \nL')
f.write('RF OUTPUT POWER CALIBRATED: not CALibrated to be done dB level -35 dBm \n')
f.write('LO LEVEL at: -6.5 dBm \n')
f.write('Shoot1 Presence of spurious dependent of Lo level \n')

#rm = resourcemanager('C:\Windows\SysWoW64')

rm = visa.ResourceManager()
rm.list_resources()
my_instrument1 = rm.open_resource('GPIB0::18::INSTR')
print(my_instrument1.query('*IDN?'))
my_instrument2 = rm.open_resource('GPIB0::28::INSTR')
print(my_instrument2.query('*IDN?'))
my_instrument3 = rm.open_resource('COM3')

print(my_instrument3.write('W-35.000'))
print(my_instrument3.query('W?'))

print(my_instrument3.write('C0E1r1\r\n'))
print(my_instrument3.write('C1E0r0\r\n'))

print(my_instrument3.write('C0r1'))
print(my_instrument1.write('CALC:MARK:STAT ON'))
# RFin start AT 11.3 GHz

# LO FREQ
FREQ_INIT = 4.48
# will start RFin at 11.3 GHz
FREQ = FREQ_INIT

FREQ_INIT = 3.28-0.025
RF_FREQ = 9-0.05
# will start RFin at 11.0 GHz
FREQ = FREQ_INIT

count = 0

# original sweep until 0.03
datetime.datetime.now()
while (FREQ < 4.38):

    FREQ = FREQ + 0.025

    RF_FREQ = RF_FREQ + 0.05
    RF_FREQ_MHz = RF_FREQ*1000

    print(RF_FREQ_MHz)
    STRING_FREQ_MHz = 'f'+str(RF_FREQ_MHz)
    print(my_instrument3.write(STRING_FREQ_MHz))
    print(my_instrument3.query('f?'))
    print('RF input:', RF_FREQ, ' GHz')
    print(my_instrument3.write('W-35.000'))

    time.sleep(1)
    STRING_FREQ = 'SOUR:FREQ '+str(FREQ)+' GHz'
    print(STRING_FREQ)

#    print(my_instrument2.write('*RST'))
    print(my_instrument2.write(STRING_FREQ))
    print(my_instrument2.write('SOUR:POWER -6.5 dBm'))
    print(my_instrument2.write('SOUR:POWER ON'))

    time.sleep(3)
#    time.sleep(0)

    print(my_instrument1.write('CALC:MARK1:MAX'))


    STR_MARKER = my_instrument1.query('CALC:MARK1:Y?')
    print(STR_MARKER)

    STR_TO_FILE = STR_MARKER
    f.write(STR_TO_FILE)

#    print('PRESS KEY')

#    input("Press Enter to continue...")

print("Good bye!")
datetime.datetime.now()
f.close()

# initializations for 1
f = open('FM_SCAN_CHANNELB', 'w')
f.write('GOM4-X PROJECT TEST3ON BOARD FM RX2 LidOn Antenna On\n')
f.write('LOSS TO IF CABLE: Not CALibrated to be done dB \nL')
f.write('RF OUTPUT POWER CALIBRATED: not CALibrated to be done dB level -35 dBm \n')
f.write('LO LEVEL at: -6.5 dBm \n')
f.write('Shoot1 Presence of spurious dependent of Lo level \n')

#rm = resourcemanager('C:\Windows\SysWoW64')

rm = visa.ResourceManager()
rm.list_resources()
my_instrument1 = rm.open_resource('GPIB0::18::INSTR')
print(my_instrument1.query('*IDN?'))
my_instrument2 = rm.open_resource('GPIB0::28::INSTR')
print(my_instrument2.query('*IDN?'))
my_instrument3 = rm.open_resource('COM3')

print(my_instrument3.write('W-35.000'))
print(my_instrument3.query('W?'))
print(my_instrument3.write('C0E0r0\r\n'))
print(my_instrument3.write('C1E1r1\r\n'))
print(my_instrument3.write('C1'))


print(my_instrument1.write('CALC:MARK:STAT ON'))
# RFin start AT 11.3 GHz

# LO FREQ
FREQ_INIT = 4.48
# will start RFin at 11.3 GHz
FREQ = FREQ_INIT

FREQ_INIT = 3.28-0.025
RF_FREQ = 9-0.05
# will start RFin at 11.0 GHz
FREQ = FREQ_INIT

count = 0

# original sweep until 0.03
datetime.datetime.now()
while (FREQ < 4.38):

    FREQ = FREQ + 0.025

    RF_FREQ = RF_FREQ + 0.05
    RF_FREQ_MHz = RF_FREQ*1000

    print(RF_FREQ_MHz)
    STRING_FREQ_MHz = 'f'+str(RF_FREQ_MHz)
    print(my_instrument3.write(STRING_FREQ_MHz))
    print(my_instrument3.query('f?'))
    print('RF input:', RF_FREQ, ' GHz')
    print(my_instrument3.write('W-35.000'))

    time.sleep(1)
    STRING_FREQ = 'SOUR:FREQ '+str(FREQ)+' GHz'
    print(STRING_FREQ)

#    print(my_instrument2.write('*RST'))
    print(my_instrument2.write(STRING_FREQ))
    print(my_instrument2.write('SOUR:POWER -6.5 dBm'))
    print(my_instrument2.write('SOUR:POWER ON'))

    time.sleep(3)
#    time.sleep(0)

    print(my_instrument1.write('CALC:MARK1:MAX'))


    STR_MARKER = my_instrument1.query('CALC:MARK1:Y?')
    print(STR_MARKER)

    STR_TO_FILE = STR_MARKER
    f.write(STR_TO_FILE)

#    print('PRESS KEY')

#    input("Press Enter to continue...")

print("Good bye!")
datetime.datetime.now()
f.close()
import pyvisa
import matplotlib.pyplot as plt
import numpy as np

rm = pyvisa.ResourceManager()
rigol = rm.open_resource('TCPIP0::192.168.1.2::INSTR')
# check that you are connected to the right rigol scope
identity = rigol.query("*IDN?") 
print(identity)
assert identity == 'RIGOL TECHNOLOGIES,MSO5104,MS5A231100810,00.01.03.00.01\n'

# setup for measurement
rigol.write(':WAV:SOUR CHAN1')
rigol.write(':WAV:MODE NORM')
rigol.write(':WAV:FORM ASC')
# take a measurement
wave = rigol.query(":WAV:DATA?")
wave = np.fromstring(wave[11:-1], sep=',')
print(wave)


plt.figure()
plt.plot(wave)
plt.show()




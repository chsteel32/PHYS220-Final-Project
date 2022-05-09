import numpy as np
import matplotlib.pyplot as plt
import sys

import PySpice
import PySpice.Logging.Logging as Logging
from PySpice.Spice.Netlist import Circuit
from PySpice.Unit import *

import scipy.fftpack as fftpack

nodes = ['n1', 'n2', 'n3']

voltage_value = 1
step_time = 1e-9

circuit = Circuit('Chaos RLDiode')

logger = Logging.setup_logging()

circuit.model('1N4001', 'D', IS=2.55E-9@u_A, RS=0.042@u_Ohm, N=1.75, TT=5.76E-6@u_s, CJO=1.85E-11@u_F, VJ=0.75@u_V, M=0.333, BV=50@u_V, IBV=1E-5@u_A, Iave=1@u_A)
circuit.SinusoidalVoltageSource('input', 'n1', circuit.gnd, amplitude=voltage_value@u_V, frequency=311@u_kHz)
circuit.Inductor('1', 'n1', 'n2', 14.16@u_mH)
circuit.Diode('1', 'n2', 'n3', model='1N4001')
circuit.Resistor('1', 'n3', circuit.gnd, 47@u_Ohm)

print("The Circuit/Netlist:\n\n", circuit)

simulator = circuit.simulator(temperature=25, nominal_temperature=25)
simulator.initial_condition(n1=0)
simulator.initial_condition(n2=0)
simulator.initial_condition(n3=0)

print('The Simulator:\n\n', simulator)

analysis = simulator.transient(start_time=0@u_s, step_time=step_time@u_s, end_time=1@u_ms)

for node in nodes:

    print('We made it to', node)

    if node == circuit.gnd or node == 'circuit.gnd':
        node = '0'

    plt.close()
    plt.figure()
    plt.title('Voltage across Node {}'.format(node))
    plt.xlabel('Time [s]')
    plt.ylabel('Voltage [V]')
    plt.grid()
    plt.plot(analysis.time, analysis[node])
    plt.savefig('chaotic_analysis_{}.jpg'.format(node), dpi=600)
    plt.show()
    plt.close()

plt.close()
plt.figure()
plt.title('Voltage across diode')
plt.xlabel('Time [s]')
plt.ylabel('Voltage [V]')
plt.grid()
plt.plot(analysis.time, (analysis['n2']-analysis['n3']))
plt.savefig('chaotic_analysis_diode_v{}.jpg'.format(voltage_value), dpi=600)
plt.show()
plt.close()

plt.close()
plt.figure()
plt.title('Phase')
plt.xlabel('V Diode')
plt.ylabel('V input')
plt.grid()
plt.plot((analysis['n2']-analysis['n3']), analysis['n1'])
plt.savefig('chaotic_analysis_phase.jpg', dpi=600)
plt.show()
plt.close()

sample_rate = 1/step_time

N = int(sample_rate*0.001)
t = np.linspace(0, 0.00001, N)

F = fftpack.rfft(analysis['n3'][:N])

f = fftpack.rfftfreq(N, 1/sample_rate)

mask = (f > 0)*(f < 1000000)

plt.close()
plt.figure()
plt.title('Frequency Domain for Chaotic behavior')
plt.plot(f[mask], abs(F[mask])/N,'g')
plt.xlabel("frequency (Hz)")
plt.savefig('chaotic_analysis_fourier.jpg', dpi=600)
plt.show()



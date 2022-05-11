import PySpice.Logging.Logging as Logging
import matplotlib.pyplot as plt
from PySpice.Spice.Netlist import Circuit
from PySpice.Unit import *
import os
import numpy as np
import PySpice.Plot.BodeDiagram as bd
import scipy.fftpack as fftpack

# os.environ['path'] += os.pathsep + r"D:\\Users\\chste\\Downloads\\ngspice-36_dll_64\\Spice64_dll\\dll-vs"


def transient_simulator(circuit, start_time, step_time, end_time, analyzed_nodes, initial_conditions):

    for current_node in initial_conditions:

        ic = initial_conditions[current_node]

        circuit.raw_spice += '.ic v({})={}@u_V'.format(current_node, ic)

        print('ic v({}) = {}'.format(current_node, ic))

    simulator = circuit.simulator(temperature=25, nominal_temperature=25)

    print(simulator)

    analysis = simulator.transient(start_time=float(start_time)@u_s, step_time=float(step_time)@u_us, end_time=float(end_time)@u_s)

    print('analysis =', analysis)
    print('analysis nodes =', analyzed_nodes)

    for node in analyzed_nodes:

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
        plt.savefig('transient_analysis_{}.jpg'.format(node), dpi=600)
        plt.show()
        plt.close()


def dc_sweep_simulator(circuit, vstart, vstop, vincr, analyzed_nodes):

    vin = np.arange(float(vstart), float(vstop), float(vincr))

    simulator = circuit.simulator(temperature=25, nominal_temperature=25)

    print(simulator)

    analysis = simulator.dc(Vinput = slice(vstart,vstop,vincr))

    print('analysis =', analysis)
    print('analysis nodes =', analyzed_nodes)

    for node in analyzed_nodes:

        print('We made it to', node)

        if node == circuit.gnd or node == 'circuit.gnd':

            node = '0'

        plt.close()
        plt.figure()
        plt.title('Voltage across Node {}'.format(node))
        plt.xlabel('Vin [s]')
        plt.ylabel('Node Voltage [V]')
        plt.grid()
        plt.plot(analysis['v-sweep'], analysis[node])
        plt.savefig('dc_analysis_{}.jpg'.format(node), dpi=600)
        plt.show()
        plt.close()


def ac_simulator(circuit, freqStart, freqStop, points, analyzed_nodes):

    

    simulator = circuit.simulator(temperature=25, nominal_temperature=25)

    print(simulator)
    
    analysis = simulator.ac(start_frequency=int(freqStart)@u_Hz, stop_frequency=int(freqStop)@u_Hz, number_of_points=points,  variation='dec')

    print('analysis =', analysis)
    print('analysis nodes =', analyzed_nodes)

    for node in analyzed_nodes:

        print('We made it to', node)

        if node == circuit.gnd or node == 'circuit.gnd':

            node = '0'

        plt.close()
        plt.figure()
        fig,axes = plt.subplots(2,figsize=(20,10))
        #plt.title('Voltage across Node {}'.format(node))
        plt.xlabel('Frequency [Hz]')
        plt.ylabel('Gain [dB]')
        plt.grid()
        
        bd.bode_diagram(axes=axes, frequency=analysis.frequency,gain=20*np.log10(np.absolute(analysis[node])),phase=np.angle(analysis[node],deg=False))
        
        plt.savefig('ac_analysis_{}.jpg'.format(node), dpi=600)
        plt.show()
        plt.close()


def chaotic_simulator(circuit, start_time, step_time, end_time, analyzed_nodes, initial_conditions):

    for current_node in initial_conditions:

        ic = initial_conditions[current_node]

        circuit.raw_spice += '.ic v({})={}@u_V'.format(current_node, ic)

        print('ic v({}) = {}'.format(current_node, ic))

    simulator = circuit.simulator(temperature=25, nominal_temperature=25)

    print(simulator)

    analysis = simulator.transient(start_time=float(start_time)@u_s, step_time=float(step_time)@u_us, end_time=float(end_time)@u_s)

    print('analysis =', analysis)
    print('analysis nodes =', analyzed_nodes)

    for node in analyzed_nodes:

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
    plt.savefig('chaotic_analysis_diode.jpg', dpi=600)
    plt.show()
    plt.close()

    plt.close()
    plt.figure()
    plt.title('Phase')
    plt.xlabel('V Diode')
    plt.ylabel('V input')
    plt.grid()
    plt.plot((analysis['n2']-analysis['n3']), analysis['n1'], lw='0.5')
    plt.savefig('chaotic_analysis_phase.jpg', dpi=600)
    plt.show()
    plt.close()

    sample_rate = 1/(float(step_time)*(10**-6))

    N = int(sample_rate*(float(end_time) - float(start_time)))
    t = np.linspace(0, 0.00001, N)

    F = fftpack.rfft(analysis['n3'][:N])

    f = fftpack.rfftfreq(N, 1/sample_rate)

    mask = (f > 0)*(f < 1000000)

    plt.figure()
    plt.plot(f[mask], abs(F[mask])/N,'g')
    plt.xlabel("frequency (Hz)")
    plt.savefig('chaotic_analysis_fourier.jpg', dpi=600)
    plt.show()

    print(circuit.elements)

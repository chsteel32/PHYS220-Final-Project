import PySpice.Logging.Logging as Logging
import matplotlib.pyplot as plt
from PySpice.Spice.Netlist import Circuit
from PySpice.Unit import *
import os
import numpy as np

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


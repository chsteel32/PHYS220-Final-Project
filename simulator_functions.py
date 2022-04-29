import PySpice.Logging.Logging as Logging
import matplotlib.pyplot as plt
from PySpice.Spice.Netlist import Circuit
from PySpice.Unit import *


def transient_simulator(circuit, start_time, step_time, end_time, analyzed_nodes):

    print(circuit)

    simulator = circuit.simulator(temperature=25, nominal_temperature=25)

    ic = 5@u_V

    simulator.initial_condition(n2=ic)

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


"""
This file is the main program to be run for using the GUI based circuit simulator

Current Capabilities:
    create circuit elements of following types
        - DC voltage source
        - resistor
        - capacitor
        - inductor
    create circuit model based on created elements
    create a pyspice netlist containing created elements

Elements to be added
    - diode
    - switch
    - AC voltage source

"""
# import packages
from tkinter import *
from PIL import ImageTk, Image
import create_element_functions as ce
import add_element_functions as ae
import simulator_functions as sf
import simulator_creators as sc
import PySpice.Logging.Logging as Logging
import matplotlib.pyplot as plt
from PySpice.Spice.Netlist import Circuit
from PySpice.Unit import *

import os

start_circuit = Circuit('COMPHYSPICE CIRCUIT')

########################################################################################################################
# #                                               FUNCTIONS                                                          # #
########################################################################################################################


# # a function which takes a desired element type and an existing pyspice circuit and uses these to create a circuit
# # element of the specified type and add this element to the given circuit
def create_element(element, circuit):

    if element == circuit_elements[0]:  # if element == 'Select Element' do nothing

        return

    elif element == circuit_elements[1]:  # if element == 'Voltage Source' create a voltage source

        # circuit is the given circuit, circuit_model_frame is the location to show the circuit model
        ce.create_voltage_source(circuit, circuit_model_frame)

    elif element == circuit_elements[2]:  # if element == 'AC Voltage Source' create an AC source

        # circuit is the given circuit, circuit_model_frame is the location to show the circuit model
        ce.create_ac_voltage_source(circuit, circuit_model_frame)

    elif element == circuit_elements[3]:  # if element == 'Resistor' create a resistor

        # circuit is the given circuit, circuit_model_frame is the location to show the circuit model
        ce.create_resistor(circuit, circuit_model_frame)

    elif element == circuit_elements[4]:  # if element == 'Capacitor' create a capacitor

        # circuit is the given circuit, circuit_model_frame is the location to show the circuit model
        ce.create_capacitor(circuit, circuit_model_frame)

    elif element == circuit_elements[5]:  # if element == 'Inductor' create an inductor

        # circuit is the given circuit, circuit_model_frame is the location to show the circuit model
        ce.create_inductor(circuit, circuit_model_frame)

    elif element == circuit_elements[6]:  # if element == 'Diode' create a diode

        # circuit is the given circuit, circuit_model_frame is the location to show the circuit model
        ce.create_diode(circuit, circuit_model_frame)

    print(circuit)


def create_simulator(simulator, circuit):

    if simulator == simulator_options[0]:

        return

    elif simulator == simulator_options[1]:

        sc.create_transient_simulator(circuit)

    elif simulator == simulator_options[2]:

        sc.create_dc_sweep_simulator(circuit)

def reset():
    global start_circuit

    try:
        os.remove("circuit.png")
        print('-----------------')
        
        ae.reset_circuit(circuit_model_frame)
        del start_circuit
        start_circuit = Circuit('COMPHYSPICE CIRCUIT')
        del ce.output_circuit
        ce.output_circuit = ae.output_circuit
        print(start_circuit)
        
        print('-----------------')
    except FileNotFoundError:
        pass
    return 

########################################################################################################################
# #                                                  MAIN PROCESSES                                                  # #
########################################################################################################################

# # create the base circuit handling using pyspice elements
logger = Logging.setup_logging()
# # create the root window using tkinter
root = Tk()
root.title('COMPHYSPICE')
root.geometry('1080x720')

menu_frame = Frame(root, width=1080, height=180)
menu_frame.grid(column=0, row=0)
menu_frame.grid_propagate(False)

display_frame = Frame(root, width=1080, height=540)
display_frame.grid(column=0, row=1)
display_frame.grid_propagate(False)

# create a tkinter frame object to house the circuit element selection menu
circuit_elements_frame = LabelFrame(menu_frame, text='Circuit Elements', padx=10, pady=10)
circuit_elements_frame.grid(column=0, row=0, padx=10, pady=5)

simulator_frame = LabelFrame(menu_frame, text='Simulator', padx=10, pady=10)
simulator_frame.grid(column=1, row=0, padx=10, pady=10)

# create a tkinter frame object to house the visual circuit model
circuit_model_frame = LabelFrame(display_frame, text='Circuit Model', padx=10, pady=10, width=780, height=420)
circuit_model_frame.pack()
# prohibit internal frame widgets from scaling (keep the circuit model centered)
circuit_model_frame.pack_propagate(False)

# define circuit element options
circuit_elements = ['Select Element',
                    'Voltage Source',
                    'AC Voltage Source',
                    'Resistor',
                    'Capacitor',
                    'Inductor',
                    'Diode']

simulator_options = ['Select Simulator',
                     'Transient Analysis',
                     'DC Sweep']

# create a tkinter variable to store the circuit element menu selection to be used when the create element button is
# clicked
selected_element = StringVar()
# set the default value of the selected element variable
selected_element.set(circuit_elements[0])

selected_simulator = StringVar()

selected_simulator.set(simulator_options[0])

# create the dropdown menu to house the possible circuit elements to be added: house this in circuit_elements_frame
OptionMenu(circuit_elements_frame, selected_element, *circuit_elements).pack()
# create the dropdown menu to house the possible simulator options
OptionMenu(simulator_frame, selected_simulator, *simulator_options).pack()
# create the button in the root window to be clicked for element creation
# when the button is clicked, an element will be created based on the circuit element selected
Button(menu_frame, text='Create Element', command=lambda: [create_element(selected_element.get(), start_circuit)]).grid(
    column=0, row=1, padx=10, pady=10)

Button(menu_frame, text='Run Simulation', command=lambda: [create_simulator(selected_simulator.get(), ce.output_circuit)]).grid(
    column=1, row=1, padx=10, pady=10)

Button(menu_frame, text='Reset', command=lambda: [reset()]).grid(
    column=2, row=1, padx=10, pady=10)

# run the main loop of the root window
root.mainloop()

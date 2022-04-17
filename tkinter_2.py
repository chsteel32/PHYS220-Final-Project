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
import tkinter_create_element_functions as ce
import PySpice.Logging.Logging as Logging
import matplotlib.pyplot as plt
from PySpice.Spice.Netlist import Circuit
from PySpice.Unit import *
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


########################################################################################################################
# #                                                  MAIN PROCESSES                                                  # #
########################################################################################################################

# # create the base circuit handling using pyspice elements
logger = Logging.setup_logging()
start_circuit = Circuit('COMPHYSPICE CIRCUIT')

# # create the root window using tkinter
root = Tk()
root.title('COMPHYSPICE')
root.geometry('1080x720')

# create a tkinter frame object to house the circuit element selection menu
circuit_elements_frame = LabelFrame(root, text='Circuit Elements', padx=10, pady=10)
circuit_elements_frame.grid(column=0, row=0)

# create a tkinter frame object to house the visual circuit model
circuit_model_frame = LabelFrame(root, text='Circuit Model', padx=10, pady=10, width=780, height=420)
circuit_model_frame.grid(column=1, row=2)
# prohibit internal frame widgets from scaling (keep the circuit model centered)
circuit_model_frame.pack_propagate(False)

# define circuit element options
circuit_elements = ['Select Element',
                    'Voltage Source',
                    'AC Voltage Source',
                    'Resistor',
                    'Capacitor',
                    'Inductor',
                    'Diode',
                    'Switch']

# create a tkinter variable to store the circuit element menu selection to be used when the create element button is
# clicked
selected_element = StringVar()
# set the default value of the selected element variable
selected_element.set(circuit_elements[0])

# create the dropdown menu to house the possible circuit elements to be added: house this in circuit_elements_frame
OptionMenu(circuit_elements_frame, selected_element, *circuit_elements).pack()
# create the button in the root window to be clicked for element creation
# when the button is clicked, an element will be created based on the circuit element selected
Button(root, text='Create Element', command=lambda: [create_element(selected_element.get(), start_circuit)]).grid(
    column=0, row=1)

# run the main loop of the root window
root.mainloop()

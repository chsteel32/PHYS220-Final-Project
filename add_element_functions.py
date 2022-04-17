"""
This file contains the functions necessary functions to draw the circuit model and add the elements to the necessary
netlist
"""
# import packages
from tkinter import *
import schemdraw
import schemdraw.elements as elm
from PIL import ImageTk, Image
import PySpice
import PySpice.Logging.Logging as Logging
from PySpice.Spice.Netlist import Circuit, SubCircuit
from PySpice.Unit import *

# A drawing on which to place the circuit elements for the circuit model
d = schemdraw.Drawing(file='circuit.png')

# create a list of circuit nodes to be used in creating the circuit diagram
circuit_nodes = []


# # A function to show the circuit model: requires the circuit_model_frame as an argument
def show_circuit(frame):

    # try the following
    try:
        # destroy the existing widgets withing the circuit_model_frame. This ensures only one model will be displayed
        # at a time
        for widget in frame.winfo_children():
            widget.destroy()
        # open the desired image (saved as circuit.png) using the PIL operations necessary for displaying images in
        # tkinter
        circuit_model = ImageTk.PhotoImage(Image.open('circuit.png'))
        # create a label in the model frame to house the image
        circuit_model_label = Label(frame)
        # root the image in the label so that it will show on the app
        circuit_model_label.image = circuit_model
        # set the label image to be the desired image
        circuit_model_label.config(image=circuit_model)
        # place the image at the center of the model frame
        circuit_model_label.place(x=390, y=210, anchor='center')
    # if you cannot perform the above, display that the file was not found and pass
    except FileNotFoundError:
        print('no file')
        pass


def node_add(node):

    if node not in circuit_nodes:

        if node != 'circuit.gnd':

            d.add(elm.Dot().label(str(node)))

        elif node == 'circuit.gnd':

            d.add(elm.Ground())

    elif node in circuit_nodes:

        print('previous node')

        for i in range(len(circuit_nodes)):

            print(d.elements[i]['label'])


# # A function to add a voltage source to the given circuit (uses information from create_voltage_source() in
# # tkinter_create_element_functions)
def add_voltage_source(voltage_name, voltage_value, first_node, second_node, circuit, direction, frame):

    # check if either node was set equal to the ground - if so, use the proper PySpice ground syntax for the node
    if second_node == 'circuit.gnd' or first_node == 'circuit.gnd':

        circuit.V(voltage_name, first_node, circuit.gnd, float(voltage_value)@u_V)

    # otherwise, add the element with whatever user input values were received for both nodes
    else:

        circuit.V(voltage_name, first_node, second_node, float(voltage_value)@u_V)

    print(circuit)

    # check the direction chosen is up
    if direction == 'Up':

        node_add(first_node)

        # use the schemdraw builtin function add to add the voltage source to the circuit model
        d.add(elm.SourceV().up().label('V' + voltage_name + ' ' + str(voltage_value) + 'V'))

        node_add(second_node)

    # check the direction chosen is down
    elif direction == 'Down':

        # use the schemdraw builtin function add to add the voltage source to the circuit model
        d.add(elm.SourceV().down().label('V' + voltage_name + ' ' + str(voltage_value) + 'V'))

    # check the direction chosen is left
    elif direction == 'Left':

        # use the schemdraw builtin function add to add the voltage source to the circuit model
        d.add(elm.SourceV().left().label('V' + voltage_name + ' ' + str(voltage_value) + 'V'))

    # check the direction chosen is right
    elif direction == 'Right':

        # use the schemdraw builtin function add to add the voltage source to the circuit model
        d.add(elm.SourceV().right().label('V' + voltage_name + ' ' + str(voltage_value) + 'V'))

    d.save('circuit.png')

    # run the function show_circuit() to display the circuit model in the circuit model frame
    show_circuit(frame)

    return circuit


# # A function to add a resistor to the given circuit (uses information from create_voltage_source() in
# # tkinter_create_element_functions)
def add_resistor(resistor_name, resistor_value, first_node, second_node, circuit, direction, frame):

    # check if either node was set equal to the ground - if so, use the proper PySpice ground syntax for the node
    if second_node == 'circuit.gnd' or first_node == 'circuit.gnd':

        circuit.R(resistor_name, first_node, circuit.gnd, float(resistor_value)@u_kOhm)

    # otherwise, add the element with whatever user input values were received for both nodes
    else:

        circuit.R(resistor_name, first_node, second_node, float(resistor_value)@u_kOhm)

    print(circuit)

    return circuit


# # A function to add a capacitor to the given circuit (uses information from create_voltage_source() in
# # tkinter_create_element_functions)
def add_capacitor(capacitor_name, capacitor_value, first_node, second_node, circuit, direction, frame):

    if second_node == 'circuit.gnd' or first_node == 'circuit.gnd':

        circuit.C(capacitor_name, first_node, circuit.gnd, float(capacitor_value)@u_uF)

    else:

        circuit.C(capacitor_name, first_node, second_node, float(capacitor_value)@u_uF)

    print(circuit)

    return circuit


# # A function to add an inductor to the given circuit (uses information from create_voltage_source() in
# # tkinter_create_element_functions)
def add_inductor(inductor_name, inductor_value, first_node, second_node, circuit, direction, frame):

    # check if either node was set equal to the ground - if so, use the proper PySpice ground syntax for the node
    if second_node == 'circuit.gnd' or first_node == 'circuit.gnd':

        circuit.L(inductor_name, first_node, circuit.gnd, float(inductor_value)@u_H)

    # otherwise, add the element with whatever user input values were received for both nodes
    else:

        circuit.L(inductor_name, first_node, second_node, float(inductor_value)@u_H)

    print(circuit)

    return circuit


# # A function to add a diode to the given circuit (uses information from create_voltage_source() in
# # tkinter_create_element_functions)
def add_diode(diode_name, diode_model, first_node, second_node, circuit, frame):

    return diode_model


# # A function to add a switch to the given circuit (uses information from create_voltage_source() in
# # tkinter_create_element_functions)
def add_switch(switch_name, starting_position, first_node, second_node, circuit, direction, frame):

    return starting_position

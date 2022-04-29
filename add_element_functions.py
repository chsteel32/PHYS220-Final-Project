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

# create a dictionary of circuit nodes to be used in creating the circuit diagram
circuit_nodes = {}

output_circuit = None


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

            circuit_nodes[node] = d.here

            return d.here, True

        elif node == 'circuit.gnd':

            d.add(elm.Ground())

            circuit_nodes[node] = d.here

            return d.here, True

    elif node in circuit_nodes:

        for previous_node in circuit_nodes:

            if previous_node == node:

                d.here = circuit_nodes[previous_node]

                return d.here, False


# # A function to add a voltage source to the given circuit (uses information from create_voltage_source() in
# # tkinter_create_element_functions)
def add_voltage_source(voltage_name, voltage_value, first_node, second_node, circuit, direction, frame):

    global output_circuit

    # check if either node was set equal to the ground - if so, use the proper PySpice ground syntax for the node
    if second_node == 'circuit.gnd':

        circuit.V(voltage_name, first_node, circuit.gnd, float(voltage_value)@u_V)

    elif first_node == 'circuit.gnd':

        circuit.V(voltage_name, circuit.gnd, second_node, float(voltage_value) @ u_V)

    # otherwise, add the element with whatever user input values were received for both nodes
    else:

        circuit.V(voltage_name, first_node, second_node, float(voltage_value)@u_V)

    print(circuit)

    first_node_location, first_node_new = node_add(first_node)

    # check the direction chosen is up
    if direction == 'Up':

        # use the schemdraw builtin function add to add the voltage source to the circuit model
        d.add(elm.SourceV().at(first_node_location).up().label('V' + voltage_name + ' ' + str(voltage_value) + 'V'))

    # check the direction chosen is down
    elif direction == 'Down':

        # use the schemdraw builtin function add to add the voltage source to the circuit model
        d.add(elm.SourceV().at(first_node_location).down().label('V' + voltage_name + ' ' + str(voltage_value) + 'V'))

    # check the direction chosen is left
    elif direction == 'Left':

        # use the schemdraw builtin function add to add the voltage source to the circuit model
        d.add(elm.SourceV().at(first_node_location).left().label('V' + voltage_name + ' ' + str(voltage_value) + 'V'))

    # check the direction chosen is right
    elif direction == 'Right':

        # use the schemdraw builtin function add to add the voltage source to the circuit model
        d.add(elm.SourceV().at(first_node_location).right().label('V' + voltage_name + ' ' + str(voltage_value) + 'V'))

    end_element = d.here

    second_node_location, second_node_new = node_add(second_node)

    if not second_node_new:

        d.add(elm.Wire('|-').at(end_element).to(second_node_location))

    d.save('circuit.png')

    # run the function show_circuit() to display the circuit model in the circuit model frame
    show_circuit(frame)

    output_circuit = circuit

    return circuit


# # A function to add a voltage source to the given circuit (uses information from create_voltage_source() in
# # tkinter_create_element_functions)
def add_ac_voltage_source(voltage_name, ac_type, voltage_value, voltage_frequency, first_node, second_node, circuit, direction, frame):

    global output_circuit

    if ac_type == 'Sinusoidal Voltage':

        # check if either node was set equal to the ground - if so, use the proper PySpice ground syntax for the node
        if second_node == 'circuit.gnd':

            circuit.SinusoidalVoltageSource(voltage_name, first_node, circuit.gnd, amplitude=float(voltage_value)@u_V, frequency=float(voltage_frequency)@u_Hz)

        elif first_node == 'circuit.gnd':

            circuit.SinusoidalVoltageSource(voltage_name, circuit.gnd, second_node, amplitude=float(voltage_value)@u_V, frequency=float(voltage_frequency)@u_Hz)

        # otherwise, add the element with whatever user input values were received for both nodes
        else:

            circuit.SinusoidalVoltageSource(voltage_name, first_node, second_node, amplitude=float(voltage_value)@u_V, frequency=float(voltage_frequency)@u_Hz)

    elif ac_type == 'Step Voltage':

        time_volt_vals = [(0, float(voltage_value)@u_V), (1 / (2 * float(voltage_frequency))@u_s, float(voltage_value)@u_V),
                          ((1+0.0000001) / (2 * float(voltage_frequency))@u_s, 0), (1/float(voltage_frequency)@u_s, 0)]

        # check if either node was set equal to the ground - if so, use the proper PySpice ground syntax for the node
        if second_node == 'circuit.gnd':

            circuit.PieceWiseLinearVoltageSource(voltage_name, first_node, circuit.gnd, time_volt_vals, dc=float(voltage_value)@u_V)

        elif first_node == 'circuit.gnd':

            circuit.PieceWiseLinearVoltageSource(voltage_name, circuit.gnd, second_node, time_volt_vals, dc=float(voltage_value)@u_V)

        # otherwise, add the element with whatever user input values were received for both nodes
        else:

            circuit.PieceWiseLinearVoltageSource(voltage_name, first_node, second_node, time_volt_vals)

    print(circuit)

    first_node_location, first_node_new = node_add(first_node)

    # check the direction chosen is up
    if direction == 'Up':

        # use the schemdraw builtin function add to add the voltage source to the circuit model
        d.add(elm.SourceControlledV().at(first_node_location).up().label('V' + voltage_name + ' ' + str(voltage_value) + 'V'))

    # check the direction chosen is down
    elif direction == 'Down':

        # use the schemdraw builtin function add to add the voltage source to the circuit model
        d.add(elm.SourceControlledV().at(first_node_location).down().label('V' + voltage_name + ' ' + str(voltage_value) + 'V'))

    # check the direction chosen is left
    elif direction == 'Left':

        # use the schemdraw builtin function add to add the voltage source to the circuit model
        d.add(elm.SourceControlledV().at(first_node_location).left().label('V' + voltage_name + ' ' + str(voltage_value) + 'V'))

    # check the direction chosen is right
    elif direction == 'Right':

        # use the schemdraw builtin function add to add the voltage source to the circuit model
        d.add(elm.SourceControlledV().at(first_node_location).right().label('V' + voltage_name + ' ' + str(voltage_value) + 'V'))

    end_element = d.here

    second_node_location, second_node_new = node_add(second_node)

    if not second_node_new:

        d.add(elm.Wire('|-').at(end_element).to(second_node_location))

    d.save('circuit.png')
    # run the function show_circuit() to display the circuit model in the circuit model frame
    show_circuit(frame)

    output_circuit = circuit

    return circuit


# # A function to add a resistor to the given circuit (uses information from create_voltage_source() in
# # tkinter_create_element_functions)
def add_resistor(resistor_name, resistor_value, first_node, second_node, circuit, direction, frame):

    global output_circuit

    # check if either node was set equal to the ground - if so, use the proper PySpice ground syntax for the node
    if second_node == 'circuit.gnd':

        circuit.R(resistor_name, first_node, circuit.gnd, float(resistor_value)@u_kOhm)

    elif first_node == 'circuit.gnd':

        circuit.R(resistor_name, circuit.gnd, second_node, float(resistor_value)@u_kOhm)

    # otherwise, add the element with whatever user input values were received for both nodes
    else:

        circuit.R(resistor_name, first_node, second_node, float(resistor_value)@u_kOhm)

    print(circuit)

    first_node_location, first_node_new = node_add(first_node)

    # check the direction chosen is up
    if direction == 'Up':

        # use the schemdraw builtin function add to add the resistor  to the circuit model
        d.add(elm.Resistor().at(first_node_location).up().label('R' + resistor_name + ' ' + str(resistor_value) + r'$k\Omega$'))

    # check the direction chosen is down
    elif direction == 'Down':

        # use the schemdraw builtin function add to add the resistor  to the circuit model
        d.add(elm.Resistor().at(first_node_location).down().label('R' + resistor_name + ' ' + str(resistor_value) + r'$k\Omega$'))

    # check the direction chosen is left
    elif direction == 'Left':

        # use the schemdraw builtin function add to add the resistor  to the circuit model
        d.add(elm.Resistor().at(first_node_location).left().label('R' + resistor_name + ' ' + str(resistor_value) + r'$k\Omega$'))

    # check the direction chosen is right
    elif direction == 'Right':

        # use the schemdraw builtin function add to add the resistor  to the circuit model
        d.add(elm.Resistor().at(first_node_location).right().label('R' + resistor_name + ' ' + str(resistor_value) + r'$k\Omega$'))

    end_element = d.here

    second_node_location, second_node_new = node_add(second_node)

    if not second_node_new:

        d.add(elm.Wire('|-').at(end_element).to(second_node_location))

    d.save('circuit.png')

    # run the function show_circuit() to display the circuit model in the circuit model frame
    show_circuit(frame)

    output_circuit = circuit

    return circuit


# # A function to add a capacitor to the given circuit (uses information from create_voltage_source() in
# # tkinter_create_element_functions)
def add_capacitor(capacitor_name, capacitor_value, first_node, second_node, circuit, direction, frame):

    global output_circuit

    if second_node == 'circuit.gnd':

        circuit.C(capacitor_name, first_node, circuit.gnd, float(capacitor_value)@u_uF)

    elif first_node == 'circuit.gnd':

        circuit.C(capacitor_name, circuit.gnd, second_node, float(capacitor_value)@u_uF)

    else:

        circuit.C(capacitor_name, first_node, second_node, float(capacitor_value)@u_uF)

    print(circuit)

    first_node_location, first_node_new = node_add(first_node)

    # check the direction chosen is up
    if direction == 'Up':

        # use the schemdraw builtin function add to add the capacitor  to the circuit model
        d.add(elm.Capacitor().at(first_node_location).up().label(
            'C' + capacitor_name + ' ' + str(capacitor_value) + r'$\mu$F'))

    # check the direction chosen is down
    elif direction == 'Down':

        # use the schemdraw builtin function add to add the capacitor  to the circuit model
        d.add(elm.Capacitor().at(first_node_location).down().label(
            'C' + capacitor_name + ' ' + str(capacitor_value) + r'$\mu$F'))

    # check the direction chosen is left
    elif direction == 'Left':

        # use the schemdraw builtin function add to add the capacitor  to the circuit model
        d.add(elm.Capacitor().at(first_node_location).left().label(
            'C' + capacitor_name + ' ' + str(capacitor_value) + r'$\mu$F'))

    # check the direction chosen is right
    elif direction == 'Right':

        # use the schemdraw builtin function add to add the capacitor  to the circuit model
        d.add(elm.Capacitor().at(first_node_location).right().label(
            'C' + capacitor_name + ' ' + str(capacitor_value) + r'$\mu$F'))

    end_element = d.here

    second_node_location, second_node_new = node_add(second_node)

    if not second_node_new:
        d.add(elm.Wire('|-').at(end_element).to(second_node_location))

    d.save('circuit.png')

    # run the function show_circuit() to display the circuit model in the circuit model frame
    show_circuit(frame)

    output_circuit = circuit

    return circuit


# # A function to add an inductor to the given circuit (uses information from create_voltage_source() in
# # tkinter_create_element_functions)
def add_inductor(inductor_name, inductor_value, first_node, second_node, circuit, direction, frame):

    global output_circuit

    # check if either node was set equal to the ground - if so, use the proper PySpice ground syntax for the node
    if second_node == 'circuit.gnd':

        circuit.L(inductor_name, first_node, circuit.gnd, float(inductor_value)@u_H)

    elif first_node == 'circuit.gnd':

        circuit.L(inductor_name, circuit.gnd, second_node, float(inductor_value)@u_H)

    # otherwise, add the element with whatever user input values were received for both nodes
    else:

        circuit.L(inductor_name, first_node, second_node, float(inductor_value)@u_H)

    print(circuit)

    first_node_location, first_node_new = node_add(first_node)

    # check the direction chosen is up
    if direction == 'Up':

        # use the schemdraw builtin function add to add the inductor  to the circuit model
        d.add(elm.Inductor().at(first_node_location).up().label(
            'L' + inductor_name + ' ' + str(inductor_value) + r'H'))

    # check the direction chosen is down
    elif direction == 'Down':

        # use the schemdraw builtin function add to add the inductor  to the circuit model
        d.add(elm.Inductor().at(first_node_location).down().label(
            'L' + inductor_name + ' ' + str(inductor_value) + r'H'))

    # check the direction chosen is left
    elif direction == 'Left':

        # use the schemdraw builtin function add to add the inductor  to the circuit model
        d.add(elm.Inductor().at(first_node_location).left().label(
            'L' + inductor_name + ' ' + str(inductor_value) + r'H'))

    # check the direction chosen is right
    elif direction == 'Right':

        # use the schemdraw builtin function add to add the inductor  to the circuit model
        d.add(elm.Inductor().at(first_node_location).right().label(
            'L' + inductor_name + ' ' + str(inductor_value) + r'H'))

    end_element = d.here

    second_node_location, second_node_new = node_add(second_node)

    if not second_node_new:
        d.add(elm.Wire('|-').at(end_element).to(second_node_location))

    d.save('circuit.png')

    # run the function show_circuit() to display the circuit model in the circuit model frame
    show_circuit(frame)

    output_circuit = circuit

    return circuit


# # A function to add a diode to the given circuit (uses information from create_voltage_source() in
# # tkinter_create_element_functions)
def add_diode(diode_name, diode_model, first_node, second_node, circuit, direction, frame):

    global output_circuit

    # check if either node was set equal to the ground - if so, use the proper PySpice ground syntax for the node
    if second_node == 'circuit.gnd':

        circuit.Diode(diode_name, first_node, circuit.gnd, model=diode_model)

    elif first_node == 'circuit.gnd':

        circuit.Diode(diode_name, circuit.gnd, second_node, model=diode_model)

    # otherwise, add the element with whatever user input values were received for both nodes
    else:

        circuit.Diode(diode_name, first_node, second_node, model=diode_model)

    print(circuit)

    first_node_location, first_node_new = node_add(first_node)

    # check the direction chosen is up
    if direction == 'Up':

        # use the schemdraw builtin function add to add the inductor  to the circuit model
        d.add(elm.Diode().at(first_node_location).up().label('D' + diode_name))

    # check the direction chosen is down
    elif direction == 'Down':

        # use the schemdraw builtin function add to add the inductor  to the circuit model
        d.add(elm.Diode().at(first_node_location).down().label('D' + diode_name))

    # check the direction chosen is left
    elif direction == 'Left':

        # use the schemdraw builtin function add to add the inductor  to the circuit model
        d.add(elm.Diode().at(first_node_location).left().label('D' + diode_name))

    # check the direction chosen is right
    elif direction == 'Right':

        # use the schemdraw builtin function add to add the inductor  to the circuit model
        d.add(elm.Diode().at(first_node_location).right().label('D' + diode_name))

    end_element = d.here

    second_node_location, second_node_new = node_add(second_node)

    if not second_node_new:
        d.add(elm.Wire('|-').at(end_element).to(second_node_location))

    d.save('circuit.png')

    # run the function show_circuit() to display the circuit model in the circuit model frame
    show_circuit(frame)

    output_circuit = circuit

"""
This File contains the functions required to create the secondary window elements of the GUI.
It also accounts for the creation of the components which are added to the circuit netlist.
"""
# import packages
from tkinter import *
import add_element_functions as cec

# create a list of direction options to be used in the direction based drop down menu
direction_options = ['Select Direction',
                     'Up',
                     'Down',
                     'Left',
                     'Right']

# create a list of ac voltage options to be used in the ac drop down menu
ac_voltage_options = ['Select AC Voltage Type',
                      'Step Voltage',
                      'Sinusoidal Voltage']

# create a list of diode models to be used in the diode model drop down menu
diode_model_options = ['Select Diode Model',
                       '1N4148PH']

output_circuit = cec.output_circuit


# # A function used to create a voltage source for a given circuit and a given frame for displaying the circuit
def create_voltage_source(circuit, frame):

    global output_circuit

    # create the popout voltage creation window
    voltage_creator_window = Toplevel()

    # # A function to check if all text input fields are filled properly
    def check_fields(*args):

        name = string_var1.get()
        value = string_var2.get()
        node_1 = string_var3.get()
        node_2 = string_var4.get()

        # check that all text fields are filled and there is no error generated
        # if these conditions are met, enable the button to create the element
        if name and value and node_1 and node_2 and error_label['text'] == '' and direction_chosen.get() != \
                direction_options[0]:
            creation_button.config(state=NORMAL)
        # otherwise, the button remains disabled
        else:
            creation_button.config(state=DISABLED)

    # # A function to check that a numerical value is given for the value input box
    def validate_input(*args):

        try:
            float(voltage_value.get())
            error_label.config(text='')
        except ValueError:
            error_label.config(text='Voltage Value must be a number!')

    # create string variables to trace changes in the text field entry boxes
    string_var1 = StringVar(voltage_creator_window)
    string_var2 = StringVar(voltage_creator_window)
    string_var3 = StringVar(voltage_creator_window)
    string_var4 = StringVar(voltage_creator_window)
    # trace the changes of these variables corresponding to the 4 text field entry boxes
    string_var1.trace('w', check_fields)
    string_var2.trace('w', check_fields)
    string_var2.trace('w', validate_input)
    string_var3.trace('w', check_fields)
    string_var4.trace('w', check_fields)

    # create a variable corresponding to the element placement direction chosen from the dropdown menu
    direction_chosen = StringVar()
    # initialize the dropdown to be the first option
    direction_chosen.set(direction_options[0])
    # trace the changes of the direction chosen field so that a direction must be selected
    direction_chosen.trace('w', check_fields)

    # create a label for the element name input entry field
    Label(voltage_creator_window, text='Voltage Source Name: ').grid(column=0, row=0, padx=20, pady=20)
    # create a label for the element value input entry field
    Label(voltage_creator_window, text='Voltage Value (V): ').grid(column=0, row=1, padx=20, pady=20)
    # create a label for the placement direction drop down menu
    Label(voltage_creator_window, text='Placement Direction:').grid(column=0, row=2, padx=20, pady=20)
    # create a label for the first node input entry field
    Label(voltage_creator_window, text='First Attachment Node: ').grid(column=0, row=3, padx=20, pady=20)
    # create a label for the second node input entry field
    Label(voltage_creator_window, text='Second Attachment Node: ').grid(column=0, row=4, padx=20, pady=20)
    # create a label corresponding to the error label (begins empty) (if a non-float value is entered, an error message
    # is displayed)
    error_label = Label(voltage_creator_window, text='')
    error_label.grid(column=1, row=6, padx=2, pady=2)

    # create an entry field to accept a name for the element
    voltage_name = Entry(voltage_creator_window, width=10, textvariable=string_var1)
    voltage_name.grid(column=1, row=0)
    # create an entry field to accept a value for the element
    voltage_value = Entry(voltage_creator_window, width=10, textvariable=string_var2)
    voltage_value.grid(column=1, row=1)
    # create an entry field to accept the first connection node for the element
    first_node = Entry(voltage_creator_window, width=10, textvariable=string_var3)
    first_node.grid(column=1, row=3)
    # create an entry field to accept the second connection node for the element
    second_node = Entry(voltage_creator_window, width=10, textvariable=string_var4)
    second_node.grid(column=1, row=4)
    # create the dropdown menu corresponding to the element placement direction
    direction_drop_down = OptionMenu(voltage_creator_window, direction_chosen, *direction_options)
    direction_drop_down.grid(column=1, row=2)

    # create the button to be used for creating the element
    # when clicked, the button calls the corresponding creation function in the
    # tkinter_circuit_element_creator_and_drawer file feeding in the proper values input into the element creation
    # window. The creation window is also terminated when the button is pressed
    creation_button = Button(voltage_creator_window, text='Create Element', command=lambda:
                             [cec.add_voltage_source(voltage_name.get(), voltage_value.get(), first_node.get(),
                                                     second_node.get(), circuit, direction_chosen.get(), frame),
                              voltage_creator_window.destroy()], state=DISABLED)
    creation_button.grid(column=1, row=5, padx=10, pady=10)
    # insert text corresponding to the ground node as default for the second node
    first_node.insert(0, 'circuit.gnd')

    output_circuit = cec.output_circuit


# # A function used to create a voltage source for a given circuit and a given frame for displaying the circuit
def create_ac_voltage_source(circuit, frame):

    global output_circuit

    # create the popout voltage creation window
    ac_voltage_creator_window = Toplevel()

    # # A function to check if all text input fields are filled properly
    def check_fields(*args):

        name = string_var1.get()
        value = string_var2.get()
        node_1 = string_var3.get()
        node_2 = string_var4.get()

        # check that all text fields are filled and there is no error generated
        # if these conditions are met, enable the button to create the element
        if name and value and node_1 and node_2 and error_label['text'] == '' and direction_chosen.get() != \
                direction_options[0] and source_type_chosen.get() != ac_voltage_options[0]:
            creation_button.config(state=NORMAL)
        # otherwise, the button remains disabled
        else:
            creation_button.config(state=DISABLED)

    # # A function to check that a numerical value is given for the value input box
    def validate_input(*args):

        try:
            float(voltage_value.get())
            error_label.config(text='')
        except ValueError:
            error_label.config(text='Value must be a number!')

    # create string variables to trace changes in the text field entry boxes
    string_var1 = StringVar(ac_voltage_creator_window)
    string_var2 = StringVar(ac_voltage_creator_window)
    string_var3 = StringVar(ac_voltage_creator_window)
    string_var4 = StringVar(ac_voltage_creator_window)
    string_var5 = StringVar(ac_voltage_creator_window)
    # trace the changes of these variables corresponding to the 4 text field entry boxes
    string_var1.trace('w', check_fields)
    string_var2.trace('w', check_fields)
    string_var2.trace('w', validate_input)
    string_var3.trace('w', check_fields)
    string_var4.trace('w', check_fields)
    string_var5.trace('w', check_fields)
    string_var5.trace('w', validate_input)

    # create a variable corresponding to the element placement direction chosen from the dropdown menu
    direction_chosen = StringVar()
    # initialize the dropdown to be the first option
    direction_chosen.set(direction_options[0])
    # trace the changes of the direction chosen field so that a direction must be selected
    direction_chosen.trace('w', check_fields)

    source_type_chosen = StringVar()
    source_type_chosen.set(ac_voltage_options[0])
    source_type_chosen.trace('w', check_fields)

    # create a label for the element name input entry field
    Label(ac_voltage_creator_window, text='Voltage Source Name: ').grid(column=0, row=0, padx=20, pady=20)
    # create a label for the ac voltage type
    Label(ac_voltage_creator_window, text='AC Voltage Type: ').grid(column=0, row=1, padx=20, pady=20)
    # create a label for the element value input entry field
    Label(ac_voltage_creator_window, text='Voltage Amplitude (V): ').grid(column=0, row=2, padx=20, pady=20)
    # create a label for th voltage source frequency input
    Label(ac_voltage_creator_window, text='Frequency (Hz): ').grid(column=0, row=3, padx=20, pady=20)
    # create a label for the placement direction drop down menu
    Label(ac_voltage_creator_window, text='Placement Direction:').grid(column=0, row=4, padx=20, pady=20)
    # create a label for the first node input entry field
    Label(ac_voltage_creator_window, text='First Attachment Node: ').grid(column=0, row=5, padx=20, pady=20)
    # create a label for the second node input entry field
    Label(ac_voltage_creator_window, text='Second Attachment Node: ').grid(column=0, row=6, padx=20, pady=20)
    # create a label corresponding to the error label (begins empty) (if a non-float value is entered, an error message
    # is displayed)
    error_label = Label(ac_voltage_creator_window, text='')
    error_label.grid(column=1, row=7, padx=2, pady=2)

    # create an entry field to accept a name for the element
    voltage_name = Entry(ac_voltage_creator_window, width=10, textvariable=string_var1)
    voltage_name.grid(column=1, row=0)
    # create a dropdown menu to select the AC voltage type
    ac_drop_down = OptionMenu(ac_voltage_creator_window, source_type_chosen, *ac_voltage_options)
    ac_drop_down.grid(column=1, row=1)
    # create an entry field to accept a value for the element
    voltage_value = Entry(ac_voltage_creator_window, width=10, textvariable=string_var2)
    voltage_value.grid(column=1, row=2)
    # create an entry field to accept the frequency of oscillation of the AC voltage source
    voltage_frequency = Entry(ac_voltage_creator_window, width=10, textvariable=string_var5)
    voltage_frequency.grid(column=1, row=3)
    # create an entry field to accept the first connection node for the element
    first_node = Entry(ac_voltage_creator_window, width=10, textvariable=string_var3)
    first_node.grid(column=1, row=5)
    # create an entry field to accept the second connection node for the element
    second_node = Entry(ac_voltage_creator_window, width=10, textvariable=string_var4)
    second_node.grid(column=1, row=6)
    # create the dropdown menu corresponding to the element placement direction
    direction_drop_down = OptionMenu(ac_voltage_creator_window, direction_chosen, *direction_options)
    direction_drop_down.grid(column=1, row=4)

    # create the button to be used for creating the element
    # when clicked, the button calls the corresponding creation function in the
    # tkinter_circuit_element_creator_and_drawer file feeding in the proper values input into the element creation
    # window. The creation window is also terminated when the button is pressed
    creation_button = Button(ac_voltage_creator_window, text='Create Element', command=lambda:
                             [cec.add_ac_voltage_source(voltage_name.get(), source_type_chosen.get(), voltage_value.get(), voltage_frequency.get(),
                                                        first_node.get(), second_node.get(), circuit, direction_chosen.get(), frame),
                              ac_voltage_creator_window.destroy()], state=DISABLED)
    creation_button.grid(column=1, row=8, padx=10, pady=10)
    # insert text corresponding to the ground node as default for the second node
    first_node.insert(0, 'circuit.gnd')

    output_circuit = cec.output_circuit


# # A function used to create a resistor for a given circuit and a given frame for displaying the circuit
def create_resistor(circuit, frame):

    global output_circuit

    # create the popout resistor creation window
    resistor_creator_window = Toplevel()

    # # A function to check if all text input fields are filled properly
    def check_fields(*args):

        name = string_var1.get()
        value = string_var2.get()
        node_1 = string_var3.get()
        node_2 = string_var4.get()

        # check that all text fields are filled and there is no error generated
        # if these conditions are met, enable the button to create the element
        if name and value and node_1 and node_2 and error_label['text'] == '' and direction_chosen.get() != \
                direction_options[0]:
            creation_button.config(state=NORMAL)
        # otherwise, the button remains disabled
        else:
            creation_button.config(state=DISABLED)

    # # A function to check that a numerical value is given for the value input box
    def validate_input(*args):

        try:
            float(resistor_value.get())
            error_label.config(text='')
        except ValueError:
            error_label.config(text='Resistor Value must be a number!')

    # create string variables to trace changes in the text field entry boxes
    string_var1 = StringVar(resistor_creator_window)
    string_var2 = StringVar(resistor_creator_window)
    string_var3 = StringVar(resistor_creator_window)
    string_var4 = StringVar(resistor_creator_window)
    # trace the changes of these variables corresponding to the 4 text field entry boxes
    string_var1.trace('w', check_fields)
    string_var2.trace('w', check_fields)
    string_var2.trace('w', validate_input)
    string_var3.trace('w', check_fields)
    string_var4.trace('w', check_fields)

    # create a variable corresponding to the element placement direction chosen from the dropdown menu
    direction_chosen = StringVar()
    # initialize the dropdown to be the first option
    direction_chosen.set(direction_options[0])

    direction_chosen.trace('w', check_fields)

    # create a label for the element name input entry field
    Label(resistor_creator_window, text='Resistor Name: ').grid(column=0, row=0, padx=20, pady=20)
    # create a label for the element value input entry field
    Label(resistor_creator_window, text='Resistor Value (kOhms): ').grid(column=0, row=1, padx=20, pady=20)
    # create a label for the placement direction drop down menu
    Label(resistor_creator_window, text='Placement Direction:').grid(column=0, row=2, padx=20, pady=20)
    # create a label for the first node input entry field
    Label(resistor_creator_window, text='First Attachment Node: ').grid(column=0, row=3, padx=20, pady=20)
    # create a label for the second node input entry field
    Label(resistor_creator_window, text='Second Attachment Node: ').grid(column=0, row=4, padx=20, pady=20)
    # create a label corresponding to the error label (begins empty) (if a non-float value is entered, an error message
    # is displayed)
    error_label = Label(resistor_creator_window, text='')
    error_label.grid(column=1, row=6, padx=2, pady=2)

    # create an entry field to accept a name for the element
    resistor_name = Entry(resistor_creator_window, width=10, textvariable=string_var1)
    resistor_name.grid(column=1, row=0)
    # create an entry field to accept a value for the element
    resistor_value = Entry(resistor_creator_window, width=10, textvariable=string_var2)
    resistor_value.grid(column=1, row=1)
    # create an entry field to accept the first connection node for the element
    first_node = Entry(resistor_creator_window, width=10, textvariable=string_var3)
    first_node.grid(column=1, row=3)
    # create an entry field to accept the second connection node for the element
    second_node = Entry(resistor_creator_window, width=10, textvariable=string_var4)
    second_node.grid(column=1, row=4)
    # create the dropdown menu corresponding to the element placement direction
    direction_drop_down = OptionMenu(resistor_creator_window, direction_chosen, *direction_options)
    direction_drop_down.grid(column=1, row=2)

    # create the button to be used for creating the element
    # when clicked, the button calls the corresponding creation function in the
    # tkinter_circuit_element_creator_and_drawer file feeding in the proper values input into the element creation
    # window. The creation window is also terminated when the button is pressed
    creation_button = Button(resistor_creator_window, text='Create Element', command=lambda:
                             [cec.add_resistor(resistor_name.get(), resistor_value.get(), first_node.get(),
                                               second_node.get(), circuit, direction_chosen.get(), frame),
                              resistor_creator_window.destroy()], state=DISABLED)
    creation_button.grid(column=1, row=5, padx=10, pady=10)
    # insert text corresponding to the ground node as default for the second node
    first_node.insert(0, 'circuit.gnd')

    output_circuit = cec.output_circuit


# # A function used to create a capacitor for a given circuit and a given frame for displaying the circuit
def create_capacitor(circuit, frame):

    global output_circuit

    # create the popout capacitor creation window
    capacitor_creator_window = Toplevel()

    # # A function to check if all text input fields are filled properly
    def check_fields(*args):

        name = string_var1.get()
        value = string_var2.get()
        node_1 = string_var3.get()
        node_2 = string_var4.get()

        # check that all text fields are filled and there is no error generated
        # if these conditions are met, enable the button to create the element
        if name and value and node_1 and node_2 and error_label['text'] == '' and direction_chosen.get() != \
                direction_options[0]:
            creation_button.config(state=NORMAL)
        # otherwise, the button remains disabled
        else:
            creation_button.config(state=DISABLED)

    # # A function to check that a numerical value is given for the value input box
    def validate_input(*args):

        try:
            float(capacitor_value.get())
            error_label.config(text='')
        except ValueError:
            error_label.config(text='Capacitor Value must be a number!')

    # create string variables to trace changes in the text field entry boxes
    string_var1 = StringVar(capacitor_creator_window)
    string_var2 = StringVar(capacitor_creator_window)
    string_var3 = StringVar(capacitor_creator_window)
    string_var4 = StringVar(capacitor_creator_window)
    # trace the changes of these variables corresponding to the 4 text field entry boxes
    string_var1.trace('w', check_fields)
    string_var2.trace('w', check_fields)
    string_var2.trace('w', validate_input)
    string_var3.trace('w', check_fields)
    string_var4.trace('w', check_fields)

    # create a variable corresponding to the element placement direction chosen from the dropdown menu
    direction_chosen = StringVar()
    # initialize the dropdown to be the first option
    direction_chosen.set(direction_options[0])

    direction_chosen.trace('w', check_fields)

    # create a label for the element name input entry field
    Label(capacitor_creator_window, text='Capacitor Name: ').grid(column=0, row=0, padx=20, pady=20)
    # create a label for the element value input entry field
    Label(capacitor_creator_window, text='Capacitor Value (uF): ').grid(column=0, row=1, padx=20, pady=20)
    # create a label for the placement direction drop down menu
    Label(capacitor_creator_window, text='Placement Direction:').grid(column=0, row=2, padx=20, pady=20)
    # create a label for the first node input entry field
    Label(capacitor_creator_window, text='First Attachment Node: ').grid(column=0, row=3, padx=20, pady=20)
    # create a label for the second node input entry field
    Label(capacitor_creator_window, text='Second Attachment Node: ').grid(column=0, row=4, padx=20, pady=20)
    # create a label corresponding to the error label (begins empty) (if a non-float value is entered, an error message
    # is displayed)
    error_label = Label(capacitor_creator_window, text='')
    error_label.grid(column=1, row=6, padx=2, pady=2)

    # create an entry field to accept a name for the element
    capacitor_name = Entry(capacitor_creator_window, width=10, textvariable=string_var1)
    capacitor_name.grid(column=1, row=0)
    # create an entry field to accept a value for the element
    capacitor_value = Entry(capacitor_creator_window, width=10, textvariable=string_var2)
    capacitor_value.grid(column=1, row=1)
    # create an entry field to accept the first connection node for the element
    first_node = Entry(capacitor_creator_window, width=10, textvariable=string_var3)
    first_node.grid(column=1, row=3)
    # create an entry field to accept the second connection node for the element
    second_node = Entry(capacitor_creator_window, width=10, textvariable=string_var4)
    second_node.grid(column=1, row=4)
    # create the dropdown menu corresponding to the element placement direction
    direction_drop_down = OptionMenu(capacitor_creator_window, direction_chosen, *direction_options)
    direction_drop_down.grid(column=1, row=2)

    # create the button to be used for creating the element
    # when clicked, the button calls the corresponding creation function in the
    # tkinter_circuit_element_creator_and_drawer file feeding in the proper values input into the element creation
    # window. The creation window is also terminated when the button is pressed
    creation_button = Button(capacitor_creator_window, text='Create Element', command=lambda:
                             [cec.add_capacitor(capacitor_name.get(), capacitor_value.get(), first_node.get(),
                                                second_node.get(), circuit, direction_chosen.get(), frame),
                              capacitor_creator_window.destroy()], state=DISABLED)
    creation_button.grid(column=1, row=5, padx=10, pady=10)
    # insert text corresponding to the ground node as default for the second node
    first_node.insert(0, 'circuit.gnd')

    output_circuit = cec.output_circuit


# # A function used to create an inductor for a given circuit and a given frame for displaying the circuit
def create_inductor(circuit, frame):

    global output_circuit

    # create the popout inductor creation window
    inductor_creator_window = Toplevel()

    # # A function to check if all text input fields are filled properly
    def check_fields(*args):

        name = string_var1.get()
        value = string_var2.get()
        node_1 = string_var3.get()
        node_2 = string_var4.get()

        # check that all text fields are filled and there is no error generated
        # if these conditions are met, enable the button to create the element
        if name and value and node_1 and node_2 and error_label['text'] == '' and direction_chosen.get() != \
                direction_options[0]:
            creation_button.config(state=NORMAL)
        # otherwise, the button remains disabled
        else:
            creation_button.config(state=DISABLED)

    # # A function to check that a numerical value is given for the value input box
    def validate_input(*args):

        try:
            float(inductor_value.get())
            error_label.config(text='')
        except ValueError:
            error_label.config(text='Inductor Value must be a number!')

    # create string variables to trace changes in the text field entry boxes
    string_var1 = StringVar(inductor_creator_window)
    string_var2 = StringVar(inductor_creator_window)
    string_var3 = StringVar(inductor_creator_window)
    string_var4 = StringVar(inductor_creator_window)
    # trace the changes of these variables corresponding to the 4 text field entry boxes
    string_var1.trace('w', check_fields)
    string_var2.trace('w', check_fields)
    string_var2.trace('w', validate_input)
    string_var3.trace('w', check_fields)
    string_var4.trace('w', check_fields)

    # create a variable corresponding to the element placement direction chosen from the dropdown menu
    direction_chosen = StringVar()
    # initialize the dropdown to be the first option
    direction_chosen.set(direction_options[0])

    direction_chosen.trace('w', check_fields)

    # create a label for the element name input entry field
    Label(inductor_creator_window, text='Inductor Name: ').grid(column=0, row=0, padx=20, pady=20)
    # create a label for the element value input entry field
    Label(inductor_creator_window, text='Inductor Value (H): ').grid(column=0, row=1, padx=20, pady=20)
    # create a label for the placement direction drop down menu
    Label(inductor_creator_window, text='Placement Direction:').grid(column=0, row=2, padx=20, pady=20)
    # create a label for the first node input entry field
    Label(inductor_creator_window, text='First Attachment Node: ').grid(column=0, row=3, padx=20, pady=20)
    # create a label for the second node input entry field
    Label(inductor_creator_window, text='Second Attachment Node: ').grid(column=0, row=4, padx=20, pady=20)
    # create a label corresponding to the error label (begins empty) (if a non-float value is entered, an error message
    # is displayed)
    error_label = Label(inductor_creator_window, text='')
    error_label.grid(column=1, row=6, padx=2, pady=2)

    # create an entry field to accept a name for the element
    inductor_name = Entry(inductor_creator_window, width=10, textvariable=string_var1)
    inductor_name.grid(column=1, row=0)
    # create an entry field to accept a value for the element
    inductor_value = Entry(inductor_creator_window, width=10, textvariable=string_var2)
    inductor_value.grid(column=1, row=1)
    # create an entry field to accept the first connection node for the element
    first_node = Entry(inductor_creator_window, width=10, textvariable=string_var3)
    first_node.grid(column=1, row=3)
    # create an entry field to accept the second connection node for the element
    second_node = Entry(inductor_creator_window, width=10, textvariable=string_var4)
    second_node.grid(column=1, row=4)
    # create the dropdown menu corresponding to the element placement direction
    direction_drop_down = OptionMenu(inductor_creator_window, direction_chosen, *direction_options)
    direction_drop_down.grid(column=1, row=2)

    # create the button to be used for creating the element
    # when clicked, the button calls the corresponding creation function in the
    # tkinter_circuit_element_creator_and_drawer file feeding in the proper values input into the element creation
    # window. The creation window is also terminated when the button is pressed
    creation_button = Button(inductor_creator_window, text='Create Element', command=lambda:
                             [cec.add_inductor(inductor_name.get(), inductor_value.get(), first_node.get(),
                                               second_node.get(), circuit, direction_chosen.get(), frame),
                              inductor_creator_window.destroy()], state=DISABLED)
    creation_button.grid(column=1, row=5, padx=10, pady=10)
    # insert text corresponding to the ground node as default for the second node
    first_node.insert(0, 'circuit.gnd')

    output_circuit = cec.output_circuit


# # A function used to create a diode for a given circuit and a given frame for displaying the circuit
def create_diode(circuit, frame):

    global output_circuit

    # create a diode model variable to correspond to the diode model selected
    diode_model = StringVar()
    # initialize the model to be the first option
    diode_model.set(diode_model_options[0])

    # create the popout inductor creation window
    diode_creator_window = Toplevel()

    # # A function to check if all text input fields are filled properly
    def check_fields(*args):
        name = string_var1.get()
        node_1 = string_var3.get()
        node_2 = string_var4.get()

        # check that all text fields are filled and there is no error generated
        # if these conditions are met, enable the button to create the element
        if name and diode_model.get() != 'Select Diode Model' and node_1 and node_2:
            creation_button.config(state=NORMAL)
        # otherwise, the button remains disabled
        else:
            creation_button.config(state=DISABLED)

    # create string variables to trace changes in the text field entry boxes
    string_var1 = StringVar(diode_creator_window)
    string_var3 = StringVar(diode_creator_window)
    string_var4 = StringVar(diode_creator_window)
    # trace the changes of these variables corresponding to the 4 text field entry boxes
    string_var1.trace('w', check_fields)
    string_var3.trace('w', check_fields)
    string_var4.trace('w', check_fields)

    # create a variable corresponding to the element placement direction chosen from the dropdown menu
    direction_chosen = StringVar()
    # initialize the dropdown to be the first option
    direction_chosen.set(direction_options[0])

    # create a label for the element name input entry field
    Label(diode_creator_window, text='Diode Name: ').grid(column=0, row=0, padx=20, pady=20)
    # create a label for the diode model dropdown menu
    Label(diode_creator_window, text='Diode Model: ').grid(column=0, row=1, padx=20, pady=20)
    # create a label for the placement direction drop down menu
    Label(diode_creator_window, text='Placement Direction:').grid(column=0, row=2, padx=20, pady=20)
    # create a label for the first node input entry field
    Label(diode_creator_window, text='First Attachment Node: ').grid(column=0, row=3, padx=20, pady=20)
    # create a label for the second node input entry field
    Label(diode_creator_window, text='Second Attachment Node: ').grid(column=0, row=4, padx=20, pady=20)

    # create an entry field to accept a name for the element
    diode_name = Entry(diode_creator_window, width=10, textvariable=string_var1)
    diode_name.grid(column=1, row=0)
    # create the dropdown menu corresponding to the diode model
    model_menu = OptionMenu(diode_creator_window, diode_model, *diode_model_options)
    model_menu.grid(column=1, row=1)
    # create an entry field to accept the first connection node for the element
    first_node = Entry(diode_creator_window, width=10, textvariable=string_var3)
    first_node.grid(column=1, row=3)
    # create an entry field to accept the second connection node for the element
    second_node = Entry(diode_creator_window, width=10, textvariable=string_var4)
    second_node.grid(column=1, row=4)
    # create the dropdown menu corresponding to the element placement direction
    direction_drop_down = OptionMenu(diode_creator_window, direction_chosen, *direction_options)
    direction_drop_down.grid(column=1, row=2)

    # create the button to be used for creating the element
    # when clicked, the button calls the corresponding creation function in the
    # tkinter_circuit_element_creator_and_drawer file feeding in the proper values input into the element creation
    # window. The creation window is also terminated when the button is pressed
    creation_button = Button(diode_creator_window, text='Create Element', command=lambda:
                             [cec.add_diode(diode_name.get(), diode_model.get(), first_node.get(),
                                            second_node.get(), circuit, direction_chosen.get(), frame),
                              diode_creator_window.destroy()], state=DISABLED)
    creation_button.grid(column=1, row=5, padx=10, pady=10)
    # insert text corresponding to the ground node as default for the second node
    first_node.insert(0, 'circuit.gnd')

    output_circuit = cec.output_circuit

from tkinter import *
import add_element_functions as aef
import simulator_functions as sf

circuit_ground_options = ['circuit.gnd', 'ground', 'g', 'gr', '0']


def create_string_var(current_window, trace_function_1, trace_function_2):

    string_var = StringVar(current_window)
    string_var.trace('w', trace_function_2)
    string_var.trace('w', trace_function_1)

    return string_var


def get_initial_conditions(variable_dictionary):

    init_cons = {}

    for node in variable_dictionary:

        init_cons[node] = variable_dictionary[node].get()

    return init_cons


def create_transient_simulator(circuit):

    node_check_boxes = {}
    var_vals = {}

    initial_conditions = {}
    initial_conditions_variables = {}

    def send_nodes(check_nodes, current_var_values):

        analysis_node_list = []

        print('current_var_vals:', current_var_values)

        for current_node in current_var_values:

            print(current_var_values[current_node].get())

            if current_var_values[current_node].get():

                print('analysis node =', current_node)

                analysis_node_list.append(current_node)

        return analysis_node_list

    # # A function to check if all text input fields are filled properly
    def check_fields(*args):

        start_time = string_var1.get()
        step_time = string_var2.get()
        end_time = string_var3.get()

        # check that all text fields are filled and there is no error generated
        # if these conditions are met, enable the button to create the element
        if start_time and step_time and end_time and not error_label['text']:
            simulation_button.config(state=NORMAL)
        # otherwise, the button remains disabled
        else:
            simulation_button.config(state=DISABLED)

    def validate_input(*args):

        try:
            float(start_time_value.get())
            float(step_time_value.get())
            float(end_time_value.get())
            for current_node in initial_conditions:
                float(initial_conditions[current_node].get())
            error_label.config(text='')
        except ValueError:
            error_label.config(text='Number Required')

    transient_creator_window = Toplevel()

    Label(transient_creator_window, text='Simulator Type: ').grid(column=0, row=0, padx=20, pady=20)
    Label(transient_creator_window, text='Transient').grid(column=1, row=0, padx=20, pady=20)
    Label(transient_creator_window, text='Start Time (s): ').grid(column=0, row=1, padx=20, pady=20)
    Label(transient_creator_window, text=u'Step Time (\u03bcs) ').grid(column=0, row=2, padx=20, pady=20)
    Label(transient_creator_window, text='End Time (s): ').grid(column=0, row=3, padx=20, pady=20)
    Label(transient_creator_window, text='Nodes to Analyze: ').grid(column=0, row=4, padx=20, pady=20)

    string_var1 = StringVar(transient_creator_window)
    string_var2 = StringVar(transient_creator_window)
    string_var3 = StringVar(transient_creator_window)

    string_var1.trace('w', check_fields)
    string_var2.trace('w', check_fields)
    string_var3.trace('w', check_fields)

    string_var1.trace('w', validate_input)
    string_var2.trace('w', validate_input)
    string_var3.trace('w', validate_input)

    start_time_value = Entry(transient_creator_window, width=10, textvariable=string_var1)
    start_time_value.grid(column=1, row=1)

    step_time_value = Entry(transient_creator_window, width=10, textvariable=string_var2)
    step_time_value.grid(column=1, row=2)

    end_time_value = Entry(transient_creator_window, width=10, textvariable=string_var3)
    end_time_value.grid(column=1, row=3)

    counter = 0

    for node in aef.circuit_nodes:

        current_var = IntVar()

        var_vals[node] = current_var

        if str(node).lower() in circuit_ground_options:

            pass

        else:

            current_check = Checkbutton(transient_creator_window, text='{}'.format(node), variable=current_var,
                                    justify=LEFT)

            current_check.grid(column=1, row=4+counter)
            current_check.grid_propagate(False)

            node_check_boxes[node] = current_check

            counter += 1

    Label(transient_creator_window, text='Initial Conditions (Voltage across Node): ').grid(column=0, row=4+counter)

    for node in aef.circuit_nodes:

        string_var = create_string_var(transient_creator_window, check_fields, validate_input)

        initial_conditions_variables[node] = string_var

        if str(node).lower() in circuit_ground_options:

            pass

        else:

            Label(transient_creator_window, text=node).grid(column=0, row=5+counter)
            initial_condition = Entry(transient_creator_window, width=5, textvariable=string_var)

            initial_condition.grid(column=1, row=5+counter)
            initial_condition.grid_propagate(False)

            initial_conditions[node] = initial_condition

            counter += 1

    simulation_button = Button(transient_creator_window, text='Start Simulation',
                               command=lambda: [sf.transient_simulator(circuit, start_time_value.get(),
                                                                       step_time_value.get(), end_time_value.get(),
                                                                       send_nodes(node_check_boxes, var_vals),
                                                                       get_initial_conditions(initial_conditions)),
                                                transient_creator_window.destroy()], state=DISABLED)
    simulation_button.grid(column=1, row=5+counter)

    error_label = Label(transient_creator_window, text='')
    error_label.grid(column=1, row=6+counter, padx=2, pady=2)

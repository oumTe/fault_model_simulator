import useful_functions
import registers
import fault_models
import comparing_results
import os

# First let us delete the file that contains the final result if it already exists
try:
    os.remove("output.csv")
except:
    pass

"""Initializing the registers to the values specified in the file initialisation.txt"""
registers.initialize()
while True:
    try:
        initialisation = input("Please enter the path to the prolog file.")
        array_initialisation = useful_functions.file_to_array(initialisation)  # Creating a list of instructions
        useful_functions.execute_assembly(array_initialisation)  # Executing the instruction
        useful_functions.fault_simulation_output('initial')
    except:
        print("This might be a wrong path, please try again.")
    else:
        break

"""Executing the code with no faults"""
while True:
    try:
        target = input("Please enter the path to the target code file.")
        assembly_code = useful_functions.file_to_array(target)
        useful_functions.execute_assembly(assembly_code)  # Executing the instruction
        useful_functions.fault_simulation_output('Golden')

    except:
        print("This might be a wrong path, please try again.")
    else:
        break

"""Simulating fault models"""
fault_models.skip(assembly_code, array_initialisation)  # Skip Model
fault_models.skip_and_repeat(assembly_code, array_initialisation)  # Skip and repeat model
fault_models.one_instruction_corruption(assembly_code, array_initialisation)
fault_models.two_instruction_corruption_32(assembly_code, array_initialisation)
fault_models.destination_corruption(assembly_code, array_initialisation)
fault_models.first_source_operand_replacement(assembly_code, array_initialisation)
fault_models.second_source_operand_replacement(assembly_code, array_initialisation)
fault_models.skip_and_new_execution(assembly_code, array_initialisation)
fault_models.two_instruction_corruption_16(assembly_code, array_initialisation)
fault_models.instruction_to_mov(assembly_code, array_initialisation)
fault_models.corrupting_by_adding_zeros_last_32(assembly_code, array_initialisation)
fault_models.corrupting_by_adding_zeros_last_16(assembly_code, array_initialisation)
fault_models.corrupt_skip_repeat(assembly_code, array_initialisation)
fault_models.corrupt_skip_repeat_16(assembly_code, array_initialisation)


# """Comparing results"""
decision = ''
while decision != 'R' and decision!= 'P':
        decision = input("Please type R if you want to analyse RTL simulation and P if you want to analyse physical injections.").upper()
while True:
    try:
        if decision == 'R':
            RTL = input("Please enter the path holding the RTL simulation outcomes.")
            comparing_results.compare_RTL("rtl_example.csv")
        elif decision == 'P':
            physical = input("Please enter the path holding the physical injection outcomes.")
            comparing_results.comparing_physical(physical)
    except:
        print("This might be a wrong path, please try again.")
    else:
        break
# comparing_results.comparing_results()


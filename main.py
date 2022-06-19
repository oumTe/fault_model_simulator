import useful_functions
import registers
import fault_models
import comparing_results
import os

# First let us delete the file that contains the final result if it already exists
try:
    os.remove("output.csv")
except:
    print("file doesn't exist")

"""Initializing all the registers with the value of 0"""
registers.initialize()

"""Initializing the registers to the values specified in the file initialisation.txt"""
# array_initialisation = useful_functions.file_to_array('initialisation.txt')  # Creating a list of instructions
# useful_functions.execute_assembly(array_initialisation)  # Executing the instruction
# useful_functions.fault_simulation_output('initial')

"""Executing the code with no faults"""
assembly_code = useful_functions.file_to_array('AssemblyCode.txt')
# useful_functions.execute_assembly(assembly_code)
# useful_functions.fault_simulation_output('Golden')
"""Performing fault models"""
fault_models.skip(assembly_code)  # Skip Model
fault_models.skip_and_repeat(assembly_code)  # Skip and repeat model
fault_models.one_instruction_corruption(assembly_code)
fault_models.two_instruction_corruption_32(assembly_code)
fault_models.destination_corruption(assembly_code)
fault_models.first_source_operand_replacement(assembly_code)
fault_models.second_source_operand_replacement(assembly_code)
fault_models.skip_and_new_execution(assembly_code)
fault_models.two_instruction_corruption_16(assembly_code)
"""Comparing results"""
comparing_results.comparing_results()

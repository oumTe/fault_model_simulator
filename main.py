import useful_functions
import registers
import fault_models
import comparing_results

"""Initializing all the registers with the value of 0"""
registers.initialize()

"""Initializing the registers to the values specified in the file initialisation.txt"""
array_initialisation = useful_functions.file_to_array('initialisation.txt')  # Creating a list of instructions
useful_functions.execute_assembly(array_initialisation, 'initial')  # Executing the instruction

"""Executing the code with no faults"""
array = useful_functions.file_to_array('AssemblyCode.txt')
useful_functions.execute_assembly(array, 'Golden')

"""Performing fault models"""
fault_models.skip(array)  # Skip Model
# # fault_models.operatorChange()

"""Comparing results"""
comparing_results.comparing_results()

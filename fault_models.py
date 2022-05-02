import registers
import useful_functions
import math
from assembly import *


def skip(array):
    """
        This function executes the skip fault model.

            :parameter :
                array (array) : an array of assembly code

    """
    for j in range(1, min(9, len(array))):  # The number of instructions that will be skipped
        i = 0

        while j < len(array) - i + 1:  # Exiting the code if the number of the instructions left is less than the
            # number of instructions that should be skipped

            # Copying the original code in another list so that we don't lose the initial instructions
            copy_lines = array.copy()

            if copy_lines[i - 1].find(',') < 0 and copy_lines[i - 1].find('(') > 0:  # if it is a branch instruction,
                # we will jump to the label line
                i = eval(useful_functions.update_assembly_code(copy_lines[i - 1]))

            else:
                for k in range(j):  # Skipping j instructions
                    copy_lines[i + k] = "mov(R0,R0)"

                # The header will be in format skip_NumberOfInstructionsSkipped_IndexOfFirstInstructionSkipped
                header = 'skip_' + str(k + 1) + '_' + str(i)
                registers.initialize()

                """ Updating the registers and the flags with their initial values"""
                array_initialisation = useful_functions.file_to_array(
                    'initialisation.txt')  # Creating a list of instructions
                useful_functions.execute_assembly(array_initialisation, 'initial')  # Executing the instruction

                """Executing the skip"""
                useful_functions.execute_assembly(copy_lines, header)

            i = i + 1


def one_instruction_corruption(array):
    """
        This function executes the skip and repeat fault model.

            :parameter :
                lines (array) : an array of assembly code

    """
    i = 0
    while i < len(array) - 1:
        copy_array = array.copy()

        # If the line of code or the one after has less than two arguments then we can not apply this model
        if len(useful_functions.get_arguments_of_function(array[i])) < 3 or len(
                useful_functions.get_arguments_of_function(array[i + 1])) < 3:
            i = i + 1

        else:
            # Extracting the arguments from the line of code that will be corrupted
            arguments_corrupted_function = useful_functions.get_arguments_of_function(array[i])

            # Extracting the arguments from the line of code that will be skipped
            arguments_skipped_function = useful_functions.get_arguments_of_function(array[i + 1])

            # Corrupting the arguments of the instruction i by changing he first and last arguments with those of the
            # skipped line
            arguments_corrupted_function[0] = arguments_skipped_function[0]
            arguments_corrupted_function[2] = arguments_skipped_function[2]

            # Replacing the instruction number i and i+1 with the corrupted instruction
            del copy_array[i:i + 2]
            code = array[i][:array[i].find('(') + 1] + ",".join(arguments_corrupted_function) + ')'
            copy_array.insert(i, code)

            # Updating the registers and the flags with their initial values
            registers.initialize()

            array_initialisation = useful_functions.file_to_array(
                'initialisation.txt')  # Creating a list of instructions
            useful_functions.execute_assembly(array_initialisation, 'initial')  # Executing the instruction

            # Executing the new formed code
            header = "SingleInstructionCorruption_" + str(
                i + 1)  # The header is in the form "SingleInstructionCorruption" the index of the skipped instruction
            useful_functions.execute_assembly(copy_array, header)
            i = i + 1


def two_instruction_corruption(array):
    """
        This function executes the skip and repeat fault model.

            :parameter :
                lines (array) : an array of assembly code

    """
    i = 0
    while i < len(array) - 2:
        copy_array = array.copy()

        # If the line of code, the one after or the one before has less than two arguments then we can not apply this model
        if len(useful_functions.get_arguments_of_function(array[i])) < 3 or len(
                useful_functions.get_arguments_of_function(array[i + 1])) < 3 or len(
                useful_functions.get_arguments_of_function(array[i + 2])) < 3:
            i = i + 1

        else:
            # Extracting the arguments from the line of code that will be corrupted
            arguments_first_instruction = useful_functions.get_arguments_of_function(array[i])

            # Extracting the arguments from the line of code that will be skipped
            arguments_second_instruction = useful_functions.get_arguments_of_function(array[i + 1])
            arguments_third_instruction = useful_functions.get_arguments_of_function(array[i + 2])

            # Corrupting the arguments of the instruction i by changing he first and last arguments with those of the
            # skipped line
            arguments_second_instruction[0] = arguments_first_instruction[0]
            arguments_second_instruction[2] = arguments_first_instruction[2]
            arguments_third_instruction[1] = arguments_second_instruction[1]

            # Replacing the instruction number i and i+1 with the corrupted instruction
            del copy_array[i + 1:i + 3]
            code_second_instruction = array[i + 1][:array[i + 1].find('(') + 1] + ",".join(
                arguments_second_instruction) + ')'
            copy_array.insert(i + 1, code_second_instruction)
            code_third_instruction = array[i + 1][:array[i + 1].find('(') + 1] + ",".join(
                arguments_third_instruction) + ')'

            copy_array.insert(i + 2, code_third_instruction)
            # Updating the registers and the flags with their initial values
            registers.initialize()
            array_initialisation = useful_functions.file_to_array(
                'initialisation.txt')  # Creating a list of instructions
            useful_functions.execute_assembly(array_initialisation, 'initial')  # Executing the instruction

            # Executing the new formed code
            header = "TwoInstructionsCorruption,First_" + str(
                i + 1) + "_Second_" + str(
                i + 2)  # The header is in the form "skipping" the number of instruction skipped
            useful_functions.execute_assembly(copy_array, header)
            i = i + 1

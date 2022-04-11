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
                header = 'skip_' + str(k + 1) + '_' + str(i + 1)

                """ Updating the registers and the flags with their initial values"""
                array_initialisation = useful_functions.file_to_array(
                    'initialisation.txt')  # Creating a list of instructions
                useful_functions.execute_assembly(array_initialisation, 'initial')  # Executing the instruction

                """Executing the skip"""
                useful_functions.execute_assembly(copy_lines, header)

            i = i + 1

def skip_and_repeat(array):
    """
        This function executes the skip and repeat fault model.

            :parameter :
                lines (array) : an array of assembly code

    """
    # Copying the original code in another list so that we don't lose the initial instructions
    number_of_instructions_skipped = 0

    """
        The number of skipped instructions must be less than the length of the array minus the minimum number of 
        repeated instructions 
    """
    while number_of_instructions_skipped + math.ceil(number_of_instructions_skipped / 2) <= len(array):

        number_of_instructions_skipped = number_of_instructions_skipped + 1
        # The index of the first skipped instruction  varies from 1 to length of the array minus the number of skipped
        # instructions
        for index_first_instruction_skipped in range(1, len(array) - number_of_instructions_skipped + 1):
            copy_lines = array.copy()

            for k in range(number_of_instructions_skipped):
                copy_lines.pop(index_first_instruction_skipped)  # Skipping number_of_instructions_skipped instructions

            # The number of repeated instructions varies from the round of then number of skipped instructions div 2
            # and the minimum  between the number of instruction skipped multiplied by 2 and the number of
            # instructions already executed
            for number_of_instructions_repeated in range(math.ceil(number_of_instructions_skipped / 2),
                                                         min(number_of_instructions_skipped * 2,
                                                             index_first_instruction_skipped) + 1):

                for index_first_instruction_repeated in range(0, index_first_instruction_skipped -
                                                                 number_of_instructions_repeated + 1):
                    cp1 = copy_lines.copy()
                    for b in range(number_of_instructions_repeated):
                        cp1.insert(index_first_instruction_skipped+b, array[b + index_first_instruction_repeated])

                    header = "NumInstrucskipped_" + str(number_of_instructions_skipped) + "_IndexFirstSkipped_" + str(
                        index_first_instruction_skipped) + "_NumInstrucRep_" + str(
                        number_of_instructions_repeated) + "_IndexFirstRep" + str(index_first_instruction_repeated)

                    print(header)
                    print(cp1)
                    """ Updating the registers and the flags with their initial values"""
                    array_initialisation = useful_functions.file_to_array(
                        'initialisation.txt')  # Creating a list of instructions
                    useful_functions.execute_assembly(array_initialisation, 'initial')  # Executing the instruction

                    """Executing the skip"""
                    useful_functions.execute_assembly(cp1, header)


def operator_change():
    """ Updating the registers with their initial values"""
    array_initialisation = useful_functions.file_to_array(
        'initialisation.txt')  # Creating a list of instructions from the file of initialization.
    useful_functions.execute_assembly(array_initialisation, 'initial')

    assembly_code = useful_functions.file_to_array('AssemblyCode.txt')
    for i in assembly_code:
        list_of_arguments = useful_functions.get_arguments_of_function(i)
        for j in range(len(list_of_arguments)):
            if list_of_arguments[j].isnumeric():  # Verify if the argument is numeric, so we don't have to update it
                print("num : " + list_of_arguments[j])
            else:  # If the argument is not numeric than it is a global variable, and so we have to replace its syntax
                print('not : ' + list_of_arguments[j])

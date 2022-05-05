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
        This function executes the one instruction corruption model. The destination and second source operands of an
        instruction i are replaced with those of the instruction i+1.
        Instruction i+1 is skipped.

            :parameter :
                array (array) : an array of assembly code

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
        This function executes the two instructions corruption.
        The destination and second source operands of an instruction i are replaced with those of the instruction i-1.
        the opcode and first source operand of the instruction i+1 are replaced with those of the instruction i .

            :parameter :
                array (array) : an array of assembly code

    """
    i = 0
    while i < len(array) - 2:
        copy_array = array.copy()

        # If one of the three successive instructions has less than 3 arguments we can not apply the model.
        if len(useful_functions.get_arguments_of_function(array[i])) < 3 or len(
                useful_functions.get_arguments_of_function(array[i + 1])) < 3 or len(
            useful_functions.get_arguments_of_function(array[i + 2])) < 3:
            i = i + 1

        else:
            # Extracting the arguments from the instruction number i
            arguments_first_instruction = useful_functions.get_arguments_of_function(array[i])

            # Extracting the arguments from the instruction number i + 1
            arguments_second_instruction = useful_functions.get_arguments_of_function(array[i + 1])

            # Extracting the arguments from the instruction number i + 2
            arguments_third_instruction = useful_functions.get_arguments_of_function(array[i + 2])

            # Corrupting the arguments of the instruction number i + 1
            arguments_second_instruction[0] = arguments_first_instruction[0]
            arguments_second_instruction[2] = arguments_first_instruction[2]
            # Corrupting the arguments of the instruction number i + 2
            arguments_third_instruction[1] = arguments_second_instruction[1]

            # Replacing the instruction number i+1 and i+2  with the corrupted instructions
            del copy_array[i + 1:i + 3]  # Deleting the initial insructions

            code_second_instruction = array[i + 1][:array[i + 1].find('(') + 1] + ",".join(
                arguments_second_instruction) + ')'
            copy_array.insert(i + 1, code_second_instruction)  # Corrupting instruction number i + 1

            code_third_instruction = array[i + 1][:array[i + 1].find('(') + 1] + ",".join(
                arguments_third_instruction) + ')'
            copy_array.insert(i + 2, code_third_instruction)  # Corrupting instruction number i + 2

            # Updating the registers and the flags with their initial values
            registers.initialize()
            array_initialisation = useful_functions.file_to_array(
                'initialisation.txt')  # Creating a list of instructions
            useful_functions.execute_assembly(array_initialisation, 'initial')  # Executing the instruction

            # Executing the new formed code
            header = "TwoInstructionsCorruption,First_" + str(
                i + 1) + "_Second_" + str(
                i + 2)  # The header is in the form "TwoInstructionsCorruption,First_" the number of the first
            # corrupted function , second , index of second corrupted one

            useful_functions.execute_assembly(copy_array, header)
            i = i + 1


# def skip_and_repeat(array):
#     """
#         This function executes the skip and repeat fault model.
#
#             :parameter :
#                 lines (array) : an array of assembly code
#
#     """
#     # Copying the original code in another list so that we don't lose the initial instructions
#     number_of_instructions_skipped = 0
#     """
#         The number of skipped instructions must be less than the length of the array minus the minimum number of
#         repeated instructions
#     """
#     while number_of_instructions_skipped + math.ceil(number_of_instructions_skipped / 2) <= len(array):
#
#         number_of_instructions_skipped = number_of_instructions_skipped + 1
#         # The index of the first skipped instruction  varies from 1 to length of the array minus the number of skipped
#         # instructions
#         index_first_instruction_skipped = 1
#         while index_first_instruction_skipped <= len(array) - number_of_instructions_skipped:
#             for number_of_instructions_repeated in range(math.ceil(number_of_instructions_skipped / 2),
#                                                          min(number_of_instructions_skipped * 2,
#                                                              index_first_instruction_skipped) + 1):
#                 index_first_instruction_repeated = 0
#
#                 while index_first_instruction_repeated <= index_first_instruction_skipped - number_of_instructions_repeated:
#                     Cp_array = []
#                     header = "NumInstrucskipped_" + str(number_of_instructions_skipped) + "_IndexFirstSkipped_" + str(
#                         index_first_instruction_skipped) + "_NumInstrucRep_" + str(
#                         number_of_instructions_repeated) + "_IndexFirstRep" + str(index_first_instruction_repeated)
#                     print(header)
#
#                     Cp_array = array[0:index_first_instruction_skipped]
#                     # for k in range(index_first_instruction_skipped):
#                     #     print(array[k])
#
#                     b = 0
#                     index_instruction_repeated = index_first_instruction_repeated
#                     while b < number_of_instructions_repeated and index_instruction_repeated < index_first_instruction_skipped:
#                         # print(array[index_instruction_repeated])
#                         Cp_array = Cp_array + array[index_instruction_repeated: index_instruction_repeated+1 ]
#                         if array[index_instruction_repeated].find('(') > 0 and array[index_instruction_repeated].find(
#                                 ',') < 0:
#                             i = eval(useful_functions.update_assembly_code(array[index_instruction_repeated]))
#                             index_first_instruction_repeated = i + 1
#                             b = b + 1
#                         else:
#                             index_instruction_repeated = index_instruction_repeated + 1
#                             b = b + 1
#                     Cp_array = Cp_array + array[index_first_instruction_skipped + number_of_instructions_skipped :]
#                     # for j in range(index_first_instruction_skipped + number_of_instructions_skipped, len(array)):
#                     #     print(array[j])
#
#                     if array[index_first_instruction_repeated - 1].find('(') > 0 and array[
#                         index_first_instruction_repeated - 1].find(',') < 0:
#                         print('hiiiii')
#                         i = index_first_instruction_repeated
#                         i = eval(useful_functions.update_assembly_code(array[index_first_instruction_repeated - 1]))
#                         index_first_instruction_repeated = i + 1
#                         print('here' , i)
#
#                     else:
#                         index_first_instruction_repeated = index_first_instruction_repeated + 1
#                     print(Cp_array)
#                     print("--------------------------------------------")
#
#             if array[index_first_instruction_skipped].find(',') < 0 and array[index_first_instruction_skipped].find(
#                     '(') > 0:
#                 i = index_first_instruction_skipped
#                 i = eval(useful_functions.update_assembly_code(array[index_first_instruction_skipped]))
#                 index_first_instruction_skipped = i + 1
#
#             else:
#                 index_first_instruction_skipped = index_first_instruction_skipped + 1

def skipping(array, index_skip):
    Cp_array = array[0:index_skip]
    return Cp_array


def repeating(array, index_repeat, number_to_repeat):
    Cp_array = array[index_repeat:index_repeat + number_to_repeat]
    return Cp_array


def skip_and_repeat(array):
    number_skip = 0
    while number_skip + math.ceil(number_skip / 2) <= len(array):
        number_skip = number_skip + 1
        cp_array = []
        index_skip = 1
        while index_skip + number_skip <= len(array):
            cp_array = skipping(array, index_skip)
            for number_of_repeat in range(math.ceil(number_skip / 2), number_skip * 2 + 1):
                index_repeat = 0
                cp_array2 = []
                while index_repeat + number_of_repeat - 1 < index_skip:
                    cp_array2 = repeating(array, index_repeat, number_of_repeat)
                    cp = array[index_skip + number_skip:]
                    header = "NumInstrucskipped_" + str(number_skip) + "_IndexFirstSkipped_" + str(
                        index_skip) + "_NumInstrucRep_" + str(
                        number_of_repeat) + "_IndexFirstRep" + str(index_repeat)
                    print(header)
                    print(cp_array + cp_array2 + cp)
                    print('--------------------------------------------------')
                    index_repeat = index_repeat + 1
            index_skip = index_skip + 1

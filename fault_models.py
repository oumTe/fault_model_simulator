import registers
import useful_functions
import math
from assembly import *


def changing_argument(i, j):
    """
    This function is useful for the one instruction corruption and one instruction skip model as well as two
    instructions corruption model.
    In fact, if the source operand of the corrupted function is an immediate value and receives a register Rd,
    it would deal with it as it was an immediate value equals d. And the opposite case, if it is a register, but
    it gets an immediate value "d" then if the immediate values is superior to 15 than the code would crash in the physical
    injection and will do nothing on a software simulation , if it is less than 15 then it would be changed to a
    register R"d" .

            :param i: The corrupted operand
            :param j: The replacement operand
            :return: The new value of the corrupted operand
    """

    # If the operand of the corrupted instruction is an immediate value, while the new value is a register then the
    # index of the register will be considered as an immediate value
    if i.isnumeric() and j.isnumeric() == False:
        j = j[1:]
    # If the operand of the corrupted instruction is a register, while the new value is an immediate value then the
    # immediate value, if it's less than 16, will be considered as the register index
    if i.isnumeric() == False and j.isnumeric() and int(j) <= 15:
        j = "R" + str(j)
    return j


def skip(array):
    """
        This function simulates the skip fault model.

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
                    copy_lines[i + k] = "MOV(R0,R0)"

                # The header will be in format skip_NumberOfInstructionsSkipped_IndexOfFirstInstructionSkipped
                header = 'skip_' + str(k + 1) + '_' + str(i)
                registers.initialize()

                """ Updating the registers and the flags with their initial values"""
                array_initialisation = useful_functions.file_to_array(
                    'initialisation.txt')  # Creating a list of instructions
                useful_functions.execute_assembly(array_initialisation)  # Executing the instruction
                print('---------------------------------------------')
                print(header)
                """Executing the skip"""
                useful_functions.execute_assembly(copy_lines)
                useful_functions.fault_simulation_output(header)

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

            # First we have to check if the corrupted second source operand should be an immediate value or a
            # register and update it if necessary
            arguments_skipped_function[2] = changing_argument(arguments_corrupted_function[2],
                                                              arguments_skipped_function[2])
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
            useful_functions.execute_assembly(array_initialisation)  # Executing the instruction

            # Executing the new formed code
            header = "SingleInstructionCorruption_" + str(
                i + 1)  # The header is in the form "SingleInstructionCorruption" the index of the skipped instruction
            print('---------------------------------------------')
            print(header)
            useful_functions.execute_assembly(copy_array)
            useful_functions.fault_simulation_output(header)
            i = i + 1


def two_instruction_corruption_32(array):
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
            # First we have to check if the corrupted second source operand should be an immediate value or a
            # register and update it if necessary
            arguments_first_instruction[2] = changing_argument(arguments_second_instruction[2],
                                                               arguments_first_instruction[2])
            arguments_second_instruction[2] = arguments_first_instruction[2]
            # Corrupting the arguments of the instruction number i + 2
            # First we have to check if the corrupted second source operand should be an immediate value or a
            # register and update it if necessary
            arguments_third_instruction[2] = changing_argument(arguments_second_instruction[2],
                                                               arguments_third_instruction[2])
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
            useful_functions.execute_assembly(array_initialisation)  # Executing the instruction

            # Executing the new formed code
            header = "32TwoInstructionsCorruption,First_" + str(
                i + 1) + "_Second_" + str(
                i + 2)  # The header is in the form "TwoInstructionsCorruption,First_" the number of the first
            # corrupted function , second , index of second corrupted one
            print('---------------------------------------------')
            print(header)
            useful_functions.execute_assembly(copy_array)
            useful_functions.fault_simulation_output(header)
            i = i + 1


def new_index(array, code):
    """
    The index returned by a label function is returned by this function.
        :param array: array of the assembly function.
        :param code: the branch instruction.
        :return: The new index of the instruction that should be executed.
    """
    i = 0
    i = eval(useful_functions.update_assembly_code(code))
    return i


def skipping(array, index_skip):
    """
    This function helps in the skipping process for the skip and repeat model.
    :param array: the array containing the assembly code
    :param index_skip: the index of the first skipped instruction
    :return: an array containing the assembly code above the skipped instruction.
    """
    Cp_array = array[0:index_skip]
    return Cp_array


def repeating(array, index_repeat, number_to_repeat):
    """
    This function helps in the repeating process for the skip and repeat model.
    :param array: the array containing the assembly code
    :param index_repeat: the index of the first repeated instruction
    :param number_to_repeat: number of instructions that should be repeated
    :return: an array containing the assembly code that should be repeated.
    """
    Cp_array = []  # The array that will contain the repeated instructions
    for b in range(number_to_repeat):  # We will be inserting the repeated instructions one by one
        if array[index_repeat + b].find('(') > 0 and array[index_repeat + b].find(',') < 0:  # If we face a branch
            # than the whole code bellow the branch instruction will be copied
            Cp_array = Cp_array + array[index_repeat + b:]
            break
        else:  # We insert the instruction to be repeated
            Cp_array = Cp_array + array[index_repeat + b: index_repeat + b + 1]
    return Cp_array


def skip_and_repeat(array):
    """
            This function simulates the skip and repeat fault model.

                :parameter :
                    array (array) : an array of assembly code

        """
    number_skip = 0

    # The minimum number of repeated instruction is equal to the number of skipped instructions divided by 2. So the
    # maximum of the skipped instructions is the total number of instructions minus the minimum number of repeated ones.
    while number_skip + math.ceil(number_skip / 2) <= len(array):
        number_skip = number_skip + 1
        cp_array = []
        index_skip = 1
        # The index of the first skipped instruction should not bypass the total number of instructions minus the
        # number of skipped instructions
        while index_skip + number_skip <= len(array):
            cp_array = skipping(array, index_skip)  # In an array we copy the code above the skipped instruction
            header = "index_skip" + str(index_skip)
            # The minimum number of repeated instruction is equal to the number of skipped instructions divided by 2.
            # The maximum number of repeated instruction is equal to the number of skipped instructions multiplied by 2.
            for number_of_repeat in range(math.ceil(number_skip / 2), number_skip * 2 + 1):
                index_repeat = 0
                cp_array2 = []
                # The index of the last repeated instruction should not bypass the index of the first skipped one.
                while index_repeat + number_of_repeat - 1 < index_skip:
                    cp_array2 = repeating(array, index_repeat, number_of_repeat)
                    cp = []
                    if cp_array2[len(cp_array2) - 1] != array[len(array) - 1]:
                        cp = array[index_skip + number_skip:]
                    header = "NumInstrucskipped_" + str(number_skip) + "_IndexFirstSkipped_" + str(
                        index_skip) + "_NumInstrucRep_" + str(
                        number_of_repeat) + "_IndexFirstRep_" + str(index_repeat)

                    registers.initialize()
                    array_initialisation = useful_functions.file_to_array(
                        'initialisation.txt')  # Creating a list of instructions
                    useful_functions.execute_assembly(array_initialisation)  # Executing the instruction
                    print('--------------------------------------------------')
                    print(header)
                    useful_functions.execute_assembly(cp_array)
                    useful_functions.execute_assembly(cp_array2)
                    useful_functions.execute_assembly(cp)
                    useful_functions.fault_simulation_output(header)
                    index_repeat = index_repeat + 1
            if array[index_skip].find('(') > 0 and array[index_skip].find(',') < 0:
                index_skip = new_index(array, array[index_skip])

            else:
                index_skip = index_skip + 1


def destination_corruption(array):
    """
        This function simulates the destination operand corruption.

            :parameter :
                array (array) : an array of assembly code

    """
    i = 0
    while i < len(array) - 1:
        copy_array = array.copy()

        # If one of the three successive instructions has less than 3 arguments we can not apply the model.
        if array[i].find(',') < 0 or array[i + 1].find(',') < 0:
            i = i + 1
        else:
            arguments_of_i = useful_functions.get_arguments_of_function(array[i])
            arguments_of_corrupted = useful_functions.get_arguments_of_function(array[i + 1])
            arguments_of_corrupted[0] = arguments_of_i[0]
            del copy_array[i + 1: i + 2]  # Deleting the initial insructions

            corrupted_instruction = array[i + 1][:array[i + 1].find('(') + 1] + ",".join(
                arguments_of_corrupted) + ')'
            copy_array.insert(i + 1, corrupted_instruction)  # Corrupting instruction number i + 2
            header = "DestinationOperandCorruption_" + str(i + 1)
            # Updating the registers and the flags with their initial values
            registers.initialize()
            array_initialisation = useful_functions.file_to_array(
                'initialisation.txt')  # Creating a list of instructions
            useful_functions.execute_assembly(array_initialisation)  # Executing the instruction

            # Executing the new formed code
            useful_functions.execute_assembly(copy_array)
            useful_functions.fault_simulation_output(header)
            i = i + 1


def first_source_operand_replacement(array):
    """
        This function simulates the first source operand corruption.

            :parameter :
                array (array) : an array of assembly code

    """
    i = 0
    while i < len(array) - 1:
        copy_array = array.copy()

        # If one of the three successive instructions has less than 3 arguments we can not apply the model.
        if array[i].find(',') < 0 or array[i + 1].find(',') < 0:
            i = i + 1
        else:
            arguments_of_i = useful_functions.get_arguments_of_function(array[i])
            arguments_of_corrupted = useful_functions.get_arguments_of_function(array[i + 1])
            if len(arguments_of_i) >= len(arguments_of_corrupted):
                arguments_of_corrupted[1] = changing_argument(arguments_of_corrupted[1],
                                                              arguments_of_i[1])
                del copy_array[i + 1: i + 2]  # Deleting the initial insructions
                corrupted_instruction = array[i + 1][:array[i + 1].find('(') + 1] + ",".join(
                    arguments_of_corrupted) + ')'
                copy_array.insert(i + 1, corrupted_instruction)  # Corrupting instruction number i + 2
                header = "FirstSourceOperandCorruption_" + str(i + 1)
                # Updating the registers and the flags with their initial values
                registers.initialize()
                array_initialisation = useful_functions.file_to_array(
                    'initialisation.txt')  # Creating a list of instructions
                useful_functions.execute_assembly(array_initialisation)  # Executing the instruction

                # Executing the new formed code
                useful_functions.execute_assembly(copy_array)
                useful_functions.fault_simulation_output(header)
                i = i + 1

            else:
                i = i + 1


def second_source_operand_replacement(array):
    """
        This function simulates the second source operand corruption.

            :parameter :
                array (array) : an array of assembly code

    """
    i = 0
    while i < len(array) - 1:
        copy_array = array.copy()

        # If one of the three successive instructions has less than 3 arguments we can not apply the model.
        if array[i].find(',') < 0 or array[i + 1].find(',') < 0:
            i = i + 1
        else:
            arguments_of_i = useful_functions.get_arguments_of_function(array[i])
            arguments_of_corrupted = useful_functions.get_arguments_of_function(array[i + 1])
            if len(arguments_of_i) == 3 and len(arguments_of_corrupted) == 3:
                arguments_of_corrupted[2] = changing_argument(arguments_of_corrupted[2],
                                                              arguments_of_i[2])
                header = "SecondSourceOperandCorruption_" + str(i + 1)
            elif len(arguments_of_i) == 3 and len(arguments_of_corrupted) == 2:
                arguments_of_corrupted[1] = changing_argument(arguments_of_corrupted[1],
                                                              arguments_of_i[2])
                header = "1_SecondSourceOperandCorruption_" + str(i + 1)
            elif len(arguments_of_i) == 2 and len(arguments_of_corrupted) == 3:
                arguments_of_corrupted[2] = changing_argument(arguments_of_corrupted[2],
                                                              arguments_of_i[1])
                header = "SecondSourceOperandCorruption_" + str(i + 1)

            del copy_array[i + 1: i + 2]  # Deleting the initial insructions
            corrupted_instruction = array[i + 1][:array[i + 1].find('(') + 1] + ",".join(
                arguments_of_corrupted) + ')'
            copy_array.insert(i + 1, corrupted_instruction)  # Corrupting instruction number i + 2
            # Updating the registers and the flags with their initial values
            registers.initialize()
            array_initialisation = useful_functions.file_to_array(
                'initialisation.txt')  # Creating a list of instructions
            useful_functions.execute_assembly(array_initialisation)  # Executing the instruction

            # Executing the new formed code
            useful_functions.execute_assembly(copy_array)
            useful_functions.fault_simulation_output(header)
            i = i + 1


def skip_and_new_execution(array):
    """
        This function simulates the one instruction skip and one instruction corruption model.

            :parameter :
                array (array) : an array of assembly code

    """
    # First we have to initialize the number of instructions that we will skip to 1.
    number_of_instruction_skipped = 1

    # In this case we can skip all the instructions since we will execute a new one.
    while number_of_instruction_skipped <= len(array):

        index_frst_skipped = 0  # The first instruction we will start skipping is the first one

        # The maximum index we can reach is the total number of instructions minus the number of instructions skipped
        while index_frst_skipped + number_of_instruction_skipped <= len(array):
            # We make a copy of our initial array containing the assembly instructions
            copy_array = array.copy()

            #  The last instruction we skip should be a 32-bit instruction, we ignore branches and labels as well.
            if array[index_frst_skipped + number_of_instruction_skipped - 1].find(
                    ',') < 0 or useful_functions.is_16_bit(
                array[index_frst_skipped + number_of_instruction_skipped - 1]):
                index_frst_skipped = index_frst_skipped + 1

            else:
                # Changing the assembly instruction to its encoding
                ARM_BYTECODE = useful_functions.assembly_to_encoding(
                    copy_array[index_frst_skipped + number_of_instruction_skipped - 1])
                ARM_BYTECODE = ARM_BYTECODE[2: 4]

                # Executing the instruction formed with the least 16-bit of the last instruction skipped
                new_assembly = useful_functions.encoding_to_assembly(ARM_BYTECODE)

                # Deleting the instructions that should be skipped
                del copy_array[index_frst_skipped: index_frst_skipped + number_of_instruction_skipped]
                # Inserting the new instruction formed
                copy_array.insert(index_frst_skipped, new_assembly)

                header = "Skipping_" + str(number_of_instruction_skipped) + "_indexOfFirst_" + str(index_frst_skipped)

                # Updating the registers and the flags with their initial values
                registers.initialize()
                array_initialisation = useful_functions.file_to_array(
                    'initialisation.txt')  # Creating a list of instructions
                useful_functions.execute_assembly(array_initialisation)  # Executing the instruction

                # Executing the new formed code
                copy_array = [each_string.upper() for each_string in copy_array]
                useful_functions.execute_assembly(copy_array)
                useful_functions.fault_simulation_output(header)

                index_frst_skipped = index_frst_skipped + 1
        number_of_instruction_skipped = number_of_instruction_skipped + 1


def two_instruction_corruption_16(array):
    """
        This function simulates two instruction corruption model.
        In this case, the repeated 16 bits  which is originally 16-bit instruction, is going to be part of a 32-
        bit instruction since it requires a 32-bit instruction to be executed (the most significant five bits
        are 0b11110).

            :parameter :
                array (array) : an array of assembly code

    """
    # Initializing the index of the 16-bit instruction as 0
    index_16_bit = 0

    while index_16_bit <= len(array) - 3:
        copy_array = array.copy()

        # This model requires a 16-bit instruction followed by two 32-bit instruction
        if (useful_functions.is_16_bit(array[index_16_bit]) == False) or useful_functions.is_16_bit(
                array[index_16_bit + 1]) or useful_functions.is_16_bit(array[index_16_bit + 2]):
            index_16_bit = index_16_bit + 1
        else:
            # Getting the encoding of the three instructions
            encoding_16_bit = useful_functions.assembly_to_encoding(array[index_16_bit])
            encoding_first_32 = useful_functions.assembly_to_encoding(array[index_16_bit + 1])
            encoding_second_32 = useful_functions.assembly_to_encoding(array[index_16_bit + 2])

            # Corrupting the encoding of the two 32-bit instructions
            encoding_first_32 =  encoding_first_32[0:2] + encoding_16_bit
            encoding_second_32 = encoding_first_32[0:2] + encoding_second_32[2:4]

            # Changing the corrupted instructions from encoding to arm instructions
            first_corrupted = useful_functions.encoding_to_assembly(encoding_first_32)
            second_corrupted = useful_functions.encoding_to_assembly(encoding_second_32)

            # Deleting the old two 32-bit instructions
            del copy_array[index_16_bit+1 : index_16_bit+3]
            # Inserting the new formed instructions
            copy_array.insert(index_16_bit+1, first_corrupted)
            copy_array.insert(index_16_bit + 2, second_corrupted)

            # The header is in the form " 16twoInstructionCorruption_" + index of the 16 bit instruction
            header = "16twoInstructionCorruption_" + str(index_16_bit)

            # Updating the registers and the flags with their initial values
            registers.initialize()
            array_initialisation = useful_functions.file_to_array(
                'initialisation.txt')  # Creating a list of instructions
            useful_functions.execute_assembly(array_initialisation)  # Executing the instruction

            # Executing the new formed code
            copy_array = [each_string.upper() for each_string in copy_array]
            useful_functions.execute_assembly(copy_array)
            useful_functions.fault_simulation_output(header)
            index_16_bit = index_16_bit +1

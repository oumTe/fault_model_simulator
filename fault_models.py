import registers
import useful_functions
import math
from assembly import *
import signal


def skip(array):
    """
        This function simulates the skip fault model.

            :parameter :
                array (array) : an array of assembly code

    """
    for j in range(1, min(9, len(array))):  # The number of instructions that will be skipped

        i = 0
        while i <= len(array) - j:  # Exiting the code if the number of the instructions left is less than the
            # number of instructions that should be skipped
            # Copying the original code in another list so that we don't lose the initial instructions
            copy_lines = array.copy()

            # Since the labels do not count as instructions, they should not be skipped.
            # We will use select_instructions which return a list of j indexes starting from the instruction i in the
            # array which are not labels
            list_of_index = useful_functions.select_instruction(array, j, i)

            # If the number of instructions other than labels is less than j, we do not execute it again
            if len(list_of_index) == j:
                for index in list_of_index:
                    copy_lines[index] = "MOV(R0,R0)"

                print('---------------------------------------------')
                # The header will be in format skip_NumberOfInstructionsSkipped_IndexOfFirstInstructionSkipped
                header = 'skip_' + str(j) + '_' + str(i)

                """ Updating the registers and the flags with their initial values"""
                registers.initialize()
                array_initialisation = useful_functions.file_to_array(
                    'initialisation.txt')  # Creating a list of instructions
                useful_functions.execute_assembly(array_initialisation)  # Executing the instructions

                print('---------------------------------------------')
                print(header)
                """Executing the skip"""
                useful_functions.execute_assembly(copy_lines)
                useful_functions.fault_simulation_output(header)

            i = i + 1

            # The labels do not count as instructions. If the first instruction to be skipped is a label then we go
            # to the next one
            try:
                if array[i].find('(') < 0:
                    i = i + 1
            except:
                pass


def one_instruction_corruption(array):
    """
        This function executes the one instruction corruption model while skipping j instructions.
        In this model we merge the least significant 16 bits of the instruction we corrupt with the most
        significant 16 bit of the last instruction we skip.
            :parameter :
                array (array) : an array of assembly code
    """
    i = 0  # index of corrupted instruction

    while i < len(array) - 1:
        # The instruction corrupted should be a 32 bit instruction
        if array[i].find(',') < 0 or useful_functions.is_16_bit(array[i]):
            i = i + 1

        else:
            j = 1  # Number of skipped instructions
            while j < min(len(array) - i, 17):

                # Since the labels do not count as instructions, they should not be skipped.
                # We will use select_instructions which return a list of j indexes starting from the instruction i in the
                # array which are not labels
                list_of_index = useful_functions.select_instruction(array, j, i + 1)

                if len(list_of_index) == j:
                    index_last_skipped = list_of_index[len(list_of_index) - 1]
                    # The last skipped instruction should be a 32-bit instruction
                    if array[index_last_skipped].find(',') < 0 or useful_functions.is_16_bit(array[index_last_skipped]):
                        j = j + 1

                    else:
                        copy_array = array.copy()
                        # Changing the instruction that should be corrupted and the last one skipped to their encoding
                        ARM_BYTECODE_corrupted = useful_functions.assembly_to_encoding(copy_array[i])
                        ARM_BYTECODE_last_skipped = useful_functions.assembly_to_encoding(
                            copy_array[index_last_skipped])
                        # Forming the new instruction which is the merge of the two instructions
                        ARM_BYTECODE_corrupted = ARM_BYTECODE_corrupted[0:2] + ARM_BYTECODE_last_skipped[2:4]
                        try:
                            instruction_corrupted = useful_functions.encoding_to_assembly(ARM_BYTECODE_corrupted)
                            # Deleting the j instructions and replacing the corrupted one with its new format
                            copy_array[i] = instruction_corrupted
                            for index in list_of_index:
                                copy_array[index] = "MOV(R0,R0)"

                            copy_array = [each_string.upper() for each_string in copy_array]

                            # Updating the registers and the flags with their initial values
                            registers.initialize()
                            array_initialisation = useful_functions.file_to_array(
                                'initialisation.txt')  # Creating a list of instructions
                            useful_functions.execute_assembly(array_initialisation)

                            # Simulating the fault
                            header = "SingleInstructionCorruptionAndSkip_" + str(i) + "_" + str(j)
                            # The header is in the form "SingleInstructionCorruption" the index of the corrupted instruction
                            # "_" number of skipped instructions
                            print('---------------------------------------------')
                            print(header)
                            useful_functions.execute_assembly(copy_array)
                            # useful_functions.fault_simulation_output(header)
                        except:
                            header = "CrashSingleInstructionCorruptionAndSkip_" + str(i) + "_" + str(j)
                            useful_functions.fault_simulation_output(header)

                        j = j + 1
                else:
                    j = j + 1
            i = i + 1


def destination_corruption(array):
    """
        This function simulates the destination operand corruption.

            :parameter :
                array (array) : an array of assembly code

    """
    i = 0
    while i < len(array) - 1:
        copy_array = array.copy()

        # This model is only applicable in the case of instructions that have destination operands (not applicable
        # for jumps)
        if array[i].find(',') < 0:
            i = i + 1
        else:
            # Getting the arguments of the instruction from which we will extract the new destination operand
            arguments_of_i = useful_functions.get_arguments_of_function(array[i])

            # We select one instruction starting from i+1. This step is important since it will return the first
            # instruction which is not a label
            index_of_corrupted = useful_functions.select_instruction(array, 1, i + 1)

            # The corrupted instruction should not be a jump or a label
            if array[index_of_corrupted[0]].find(',') > 0:
                # Changing the destination operand of the corrupted instruction with the new one
                arguments_of_corrupted = useful_functions.get_arguments_of_function(array[index_of_corrupted[0]])
                arguments_of_corrupted[0] = arguments_of_i[0]

                # Forming the new instruction
                corrupted_instruction = array[index_of_corrupted[0]][
                                        :array[index_of_corrupted[0]].find('(') + 1] + ",".join(
                    arguments_of_corrupted) + ')'

                # Corrupting instruction
                copy_array[index_of_corrupted[0]] = corrupted_instruction
                # Updating the registers and the flags with their initial values
                registers.initialize()
                array_initialisation = useful_functions.file_to_array(
                    'initialisation.txt')  # Creating a list of instructions
                useful_functions.execute_assembly(array_initialisation)  # Executing the instruction

                # Executing the new formed code
                header = "DestinationOperandCorruption_" + str(index_of_corrupted[0])
                print('------------------------\n', header)
                useful_functions.execute_assembly(copy_array)
                useful_functions.fault_simulation_output(header)

            i = i + 1


def first_source_operand_replacement(array):
    """
        This function simulates the destination operand corruption.

            :parameter :
                array (array) : an array of assembly code

    """
    i = 0
    while i < len(array) - 1:
        copy_array = array.copy()

        # This model is only applicable in the case of instructions that have destination operands (not applicable
        # for jumps)
        if array[i].find(',') < 0:
            i = i + 1
        else:
            # Getting the arguments of the instruction from which we will extract the new destination operand
            arguments_of_i = useful_functions.get_arguments_of_function(array[i])

            # We select one instruction starting from i+1. This step is important since it will return the first
            # instruction which is not a label
            index_of_corrupted = useful_functions.select_instruction(array, 1, i + 1)

            # The corrupted instruction should not be a jump or a label
            if array[index_of_corrupted[0]].find(',') > 0:

                # Getting the arguments of the corrupted instruction
                arguments_of_corrupted = useful_functions.get_arguments_of_function(array[index_of_corrupted[0]])

                # Case of two successive instructions with the same number of operands
                if len(arguments_of_i) == len(arguments_of_corrupted):

                    # Changing the corrupted operand with the new value
                    arguments_of_corrupted[1] = arguments_of_i[1]

                    corrupted_instruction = array[index_of_corrupted[0]][
                                            :array[index_of_corrupted[0]].find('(') + 1] + ",".join(
                        arguments_of_corrupted) + ')'

                    copy_array[index_of_corrupted[0]] = corrupted_instruction

                    # Updating the registers and the flags with their initial values
                    registers.initialize()
                    array_initialisation = useful_functions.file_to_array(
                        'initialisation.txt')  # Creating a list of instructions
                    useful_functions.execute_assembly(array_initialisation)  # Executing the instruction

                    # Executing the new formed code
                    header = "FirstSourceOperandCorruption_" + str(index_of_corrupted[0])
                    print('------------------------\n', header)
                    useful_functions.execute_assembly(copy_array)
                    useful_functions.fault_simulation_output(header)
                    i = i + 1

                # Case of a 3-operand instruction followed by 2-operand instruction
                elif len(arguments_of_i) > len(arguments_of_corrupted):
                    # Changing the corrupted operand with the new value
                    arguments_of_corrupted[1] = arguments_of_i[2]

                    corrupted_instruction = array[index_of_corrupted[0]][
                                            :array[index_of_corrupted[0]].find('(') + 1] + ",".join(
                        arguments_of_corrupted) + ')'

                    # Corrupting instruction
                    copy_array[index_of_corrupted[0]] = corrupted_instruction

                    # Updating the registers and the flags with their initial values
                    registers.initialize()
                    array_initialisation = useful_functions.file_to_array(
                        'initialisation.txt')  # Creating a list of instructions
                    useful_functions.execute_assembly(array_initialisation)  # Executing the instruction

                    # Executing the new formed code
                    header = "SourceOperandReplacement_" + str(index_of_corrupted[0])
                    print('------------------------\n', header)
                    useful_functions.execute_assembly(copy_array)
                    useful_functions.fault_simulation_output(header)
                    i = i + 1
                else:
                    i = i + 1
            else:
                i = i + 1


def second_source_operand_replacement(array):
    """
        This function simulates the destination operand corruption.

            :parameter :
                array (array) : an array of assembly code

    """
    i = 0
    while i < len(array) - 1:
        copy_array = array.copy()

        # This model is only applicable in the case of instructions that have destination operands (not applicable
        # for jumps)
        if array[i].find(',') < 0:
            i = i + 1
        else:
            # Getting the arguments of the instruction that would be used to extract the second source operand
            arguments_of_i = useful_functions.get_arguments_of_function(array[i])

            # We select one instruction starting from i+1. This step is important since it will return the first
            # instruction which is not a label
            index_of_corrupted = useful_functions.select_instruction(array, 1, i + 1)

            # The corrupted instruction should not be a jump or a label
            if array[index_of_corrupted[0]].find(',') > 0:

                # Getting the arguments of the corrupted instruction
                arguments_of_corrupted = useful_functions.get_arguments_of_function(array[index_of_corrupted[0]])

                # Case of two successive 3-operand instructions
                if len(arguments_of_i) == 3 and len(arguments_of_corrupted) == 3:
                    arguments_of_corrupted[2] = arguments_of_i[2]

                    corrupted_instruction = array[index_of_corrupted[0]][
                                            :array[index_of_corrupted[0]].find('(') + 1] + ",".join(
                        arguments_of_corrupted) + ')'

                    # Corrupting instruction
                    copy_array[index_of_corrupted[0]] = corrupted_instruction

                    # Updating the registers and the flags with their initial values
                    registers.initialize()
                    array_initialisation = useful_functions.file_to_array(
                        'initialisation.txt')  # Creating a list of instructions
                    useful_functions.execute_assembly(array_initialisation)  # Executing the instruction

                    # Executing the new formed code
                    header = "SecondSourceOperandCorruption_" + str(index_of_corrupted[0])
                    print('------------------------\n', header)
                    useful_functions.execute_assembly(copy_array)
                    useful_functions.fault_simulation_output(header)
                    i = i + 1

                # Case of 2-operand instruction followed by 3-operand instruction
                elif len(arguments_of_i) == 2 and len(arguments_of_corrupted) == 3:
                    arguments_of_corrupted[2] = arguments_of_i[1]

                    corrupted_instruction = array[index_of_corrupted[0]][
                                            :array[index_of_corrupted[0]].find('(') + 1] + ",".join(
                        arguments_of_corrupted) + ')'

                    copy_array[index_of_corrupted[0]] = corrupted_instruction

                    # Updating the registers and the flags with their initial values
                    registers.initialize()
                    array_initialisation = useful_functions.file_to_array(
                        'initialisation.txt')  # Creating a list of instructions
                    useful_functions.execute_assembly(array_initialisation)  # Executing the instruction

                    # Executing the new formed code
                    header = "SecondSourceOperandCorruption_" + str(index_of_corrupted[0])
                    print('------------------------\n', header)
                    useful_functions.execute_assembly(copy_array)
                    useful_functions.fault_simulation_output(header)
                    i = i + 1

                else:
                    i = i + 1

            else:
                i = i + 1


def skip_and_new_execution(array):
    """
            This function simulates the one instruction skip and one instruction corruption model. We skip multiple
            instructions, and executes the instruction formed with the least 16-bit of the last skipped instruction.

                :parameter :
                    array (array) : an array of assembly code

        """
    i = 0  # index of first skipped instruction

    while i < len(array) - 1:
        # The instruction corrupted should be a 32 bit instruction
        if array[i].find('(') < 0:
            i = i + 1

        else:
            j = 1  # Number of skipped instructions
            while j <= min(len(array) - i, 17):

                # Since the labels do not count as instructions, they should not be skipped.
                # We will use select_instructions which return a list of j indexes starting from the instruction i in the
                # array which are not labels
                list_of_index = useful_functions.select_instruction(array, j, i)

                if len(list_of_index) == j:
                    index_last_skipped = list_of_index[len(list_of_index) - 1]
                    # The last skipped instruction should be a 32-bit instruction
                    if array[index_last_skipped].find(',') < 0 or useful_functions.is_16_bit(
                            array[index_last_skipped]):
                        j = j + 1

                    else:
                        copy_array = array.copy()
                        # Changing the last instruction skipped to its encoding
                        ARM_BYTECODE_last_skipped = useful_functions.assembly_to_encoding(
                            copy_array[index_last_skipped])

                        # The new instruction which is formed with the least 16-bit of the last skipped instruction
                        ARM_BYTECODE_corrupted = ARM_BYTECODE_last_skipped[2:4]

                        try:
                            instruction_corrupted = useful_functions.encoding_to_assembly(ARM_BYTECODE_corrupted)
                            # Deleting the j instructions and replacing the corrupted one with its new format
                            for index in list_of_index:
                                copy_array[index] = "MOV(R0,R0)"
                            copy_array[index_last_skipped] = instruction_corrupted

                            copy_array = [each_string.upper() for each_string in copy_array]

                            # Updating the registers and the flags with their initial values
                            registers.initialize()
                            array_initialisation = useful_functions.file_to_array(
                                'initialisation.txt')  # Creating a list of instructions
                            useful_functions.execute_assembly(array_initialisation)

                            # Simulating the fault
                            header = "SkipNewExecute_" + str(i) + "_" + str(j)
                            # The header is in the form "SingleInstructionCorruption" the index of the corrupted
                            # instruction "_" number of skipped instructions
                            print('---------------------------------------------')
                            print(header)
                            useful_functions.execute_assembly(copy_array)
                            # useful_functions.fault_simulation_output(header)
                        except:
                            header = "Crash_SingleInstructionCorruptionAndSkip_" + str(i) + "_" + str(j)
                            useful_functions.fault_simulation_output(header)

                        j = j + 1
                else:
                    j = j + 1
            i = i + 1


def instruction_to_mov(array):
    """
    In this model we corrupt one instruction by changing it to mov(destination_operand, R0)
    """
    # We go through the array and each time we corrupt one instruction
    for index_of_corrupted in range(len(array)):
        copy_array = array.copy()
        # We do not include labels or jumps
        if copy_array[index_of_corrupted].find(',') < 0:
            pass

        else:
            # Getting the original arguments of the corrupted instruction
            arguments_of_corrupted = useful_functions.get_arguments_of_function(copy_array[index_of_corrupted])
            # Forming the new instruction in the form mov(destination_operand,R0)
            new_instruction = "mov(" + arguments_of_corrupted[0] + ", R0 )"

            # Changing the corrupted instruction
            copy_array[index_of_corrupted] = new_instruction
            header = "corruptingToMov_" + str(index_of_corrupted)

            # Updating the registers and the flags with their initial values
            registers.initialize()
            array_initialisation = useful_functions.file_to_array(
                'initialisation.txt')  # Creating a list of instructions
            useful_functions.execute_assembly(array_initialisation)  # Executing the instruction

            # Executing the new formed code
            copy_array = [each_string.upper() for each_string in copy_array]
            print('--------------\n', header)
            useful_functions.execute_assembly(copy_array)
            useful_functions.fault_simulation_output(header)


def corrupting_by_adding_zeros_last_32(array):
    """
        This function executes the one instruction corruption model while skipping j instructions.
        In this model we merge the least significant 16 bits of the instruction we corrupt with the most
        significant 16 bit of the last instruction we skip.
            :parameter :
                array (array) : an array of assembly code
    """
    i = 0  # index of corrupted instruction

    while i < len(array) - 1:
        # The instruction corrupted should be a 32 bit instruction
        if array[i].find(',') < 0 or useful_functions.is_16_bit(array[i]):
            i = i + 1

        else:
            j = 1  # Number of skipped instructions
            while j < min(len(array) - i, 17):

                # Since the labels do not count as instructions, they should not be skipped.
                # We will use select_instructions which return a list of j indexes starting from the instruction i in the
                # array which are not labels
                list_of_index = useful_functions.select_instruction(array, j, i + 1)

                if len(list_of_index) == j:
                    index_last_skipped = list_of_index[len(list_of_index) - 1]
                    # The last skipped instruction should be a 32-bit instruction
                    if array[index_last_skipped].find(',') < 0 or useful_functions.is_16_bit(array[index_last_skipped]):
                        j = j + 1

                    else:
                        copy_array = array.copy()
                        # Changing the instruction that should be corrupted and the last one skipped to their encoding
                        ARM_BYTECODE_corrupted = useful_functions.assembly_to_encoding(copy_array[i])
                        ARM_BYTECODE_last_skipped = useful_functions.assembly_to_encoding(
                            copy_array[index_last_skipped])
                        Zero_bytes = useful_functions.assembly_to_encoding('movs(r0,r0)')

                        # Adding zeros to the most significant 16-bit of the corrupted instruction
                        ARM_BYTECODE_corrupted = ARM_BYTECODE_corrupted[0:2] + Zero_bytes

                        # Executing only the least 16-bit of the last skipped instruction
                        ARM_BYTECODE_last_skipped = useful_functions.assembly_to_encoding(
                            copy_array[index_last_skipped])
                        ARM_BYTECODE_last_skipped = ARM_BYTECODE_last_skipped[2:4]

                        try:
                            instruction_corrupted = useful_functions.encoding_to_assembly(ARM_BYTECODE_corrupted)
                            corrupting_last_skipped = useful_functions.encoding_to_assembly(ARM_BYTECODE_last_skipped)

                            # Deleting the j instructions and replacing the corrupted ones with their new format
                            copy_array[i] = instruction_corrupted
                            for index in list_of_index:
                                copy_array[index] = "MOV(R0,R0)"

                            copy_array[index_last_skipped] = corrupting_last_skipped
                            copy_array = [each_string.upper() for each_string in copy_array]

                            # Updating the registers and the flags with their initial values
                            registers.initialize()
                            array_initialisation = useful_functions.file_to_array(
                                'initialisation.txt')  # Creating a list of instructions
                            useful_functions.execute_assembly(array_initialisation)

                            # Simulating the fault

                            header = "corruptingByAddingZerosLast32_" + str(i) + "_" + str(j)
                            # The header is in the form "corruptingByAddingZerosLast32" the index of the corrupted
                            # instruction "_" number of skipped instructions
                            print('---------------------------------------------')
                            print(header)
                            useful_functions.execute_assembly(copy_array)
                            # useful_functions.fault_simulation_output(header)
                        except:
                            header = "CrashCorruptingByAddingZerosLast32_" + str(i) + "_" + str(j)
                            useful_functions.fault_simulation_output(header)

                        j = j + 1
                else:
                    j = j + 1
            i = i + 1


def corrupting_by_adding_zeros_last_16(array):
    """
        This function executes the one instruction corruption model while skipping j instructions.
        In this model we merge the least significant 16 bits of the instruction we corrupt with the most
        significant 16 bit of the last instruction we skip.
            :parameter :
                array (array) : an array of assembly code
    """
    i = 0  # index of corrupted instruction

    while i < len(array) - 1:
        # The instruction corrupted should be a 32 bit instruction
        if array[i].find(',') < 0 or useful_functions.is_16_bit(array[i]):
            i = i + 1

        else:
            j = 1  # Number of skipped instructions
            while j < min(len(array) - i, 17):

                # Since the labels do not count as instructions, they should not be skipped.
                # We will use select_instructions which return a list of j indexes starting from the instruction i in the
                # array which are not labels
                list_of_index = useful_functions.select_instruction(array, j, i + 1)

                if len(list_of_index) == j:

                    copy_array = array.copy()
                    # Changing the instruction that should be corrupted and the last one skipped to their encoding
                    ARM_BYTECODE_corrupted = useful_functions.assembly_to_encoding(copy_array[i])
                    Zero_bytes = useful_functions.assembly_to_encoding('movs(r0,r0)')

                    # Adding zeros to the most significant 16-bit of the corrupted instruction
                    ARM_BYTECODE_corrupted = ARM_BYTECODE_corrupted[0:2] + Zero_bytes

                    try:
                        instruction_corrupted = useful_functions.encoding_to_assembly(ARM_BYTECODE_corrupted)

                        # Deleting the j instructions and replacing the corrupted one with its new format
                        copy_array[i] = instruction_corrupted
                        for index in list_of_index:
                            copy_array[index] = "MOV(R0,R0)"

                        copy_array = [each_string.upper() for each_string in copy_array]

                        # Updating the registers and the flags with their initial values
                        registers.initialize()
                        array_initialisation = useful_functions.file_to_array(
                            'initialisation.txt')  # Creating a list of instructions
                        useful_functions.execute_assembly(array_initialisation)

                        # Simulating the fault

                        header = "corruptingByAddingZerosLast16_" + str(i) + "_" + str(j)
                        # The header is in the form "corruptingByAddingZerosLast32" the index of the corrupted
                        # instruction "_" number of skipped instructions
                        print('---------------------------------------------')
                        print(header)
                        useful_functions.execute_assembly(copy_array)
                        # useful_functions.fault_simulation_output(header)
                    except:
                        header = "CrashCorruptingByAddingZerosLast16_" + str(i) + "_" + str(j)
                        useful_functions.fault_simulation_output(header)

                    j = j + 1
                else:
                    j = j + 1
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
            arguments_first_instruction[2] = useful_functions.changing_argument(arguments_second_instruction[2],
                                                                                arguments_first_instruction[2])
            arguments_second_instruction[2] = arguments_first_instruction[2]
            # Corrupting the arguments of the instruction number i + 2
            # First we have to check if the corrupted second source operand should be an immediate value or a
            # register and update it if necessary
            arguments_third_instruction[2] = useful_functions.changing_argument(arguments_second_instruction[2],
                                                                                arguments_third_instruction[2])
            arguments_third_instruction[1] = arguments_second_instruction[1]

            # Replacing the instruction number i+1 and i+2  with the corrupted instructions
            del copy_array[i + 1:i + 3]  # Deleting the initial instructions

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

        # This model requires a 16-bit instruction followed by two 32-bit instruction.
        if array[index_16_bit].find(',') < 0 or array[index_16_bit + 1].find(',') < 0:
            index_16_bit = index_16_bit + 1

        elif (useful_functions.is_16_bit(array[index_16_bit]) == False) or useful_functions.is_16_bit(
                array[index_16_bit + 1]) or useful_functions.is_16_bit(array[index_16_bit + 2]):
            index_16_bit = index_16_bit + 1

        else:
            # Getting the encoding of the three instructions
            encoding_16_bit = useful_functions.assembly_to_encoding(array[index_16_bit])
            encoding_first_32 = useful_functions.assembly_to_encoding(array[index_16_bit + 1])
            encoding_second_32 = useful_functions.assembly_to_encoding(array[index_16_bit + 2])

            # Corrupting the encoding of the two 32-bit instructions
            encoding_first_32 = encoding_first_32[0:2] + encoding_16_bit
            encoding_second_32 = encoding_first_32[0:2] + encoding_second_32[2:4]

            # Changing the corrupted instructions from encoding to arm instructions
            first_corrupted = useful_functions.encoding_to_assembly(encoding_first_32)
            second_corrupted = useful_functions.encoding_to_assembly(encoding_second_32)

            # Deleting the old two 32-bit instructions
            del copy_array[index_16_bit + 1: index_16_bit + 3]
            # Inserting the new formed instructions
            copy_array.insert(index_16_bit + 1, first_corrupted)
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
            index_16_bit = index_16_bit + 1


def corrupt_skip_repeat(array):
    number_skip = 0
    # The minimum number of instructions repeated is the half of the number of instructions skipped
    while number_skip <= len(array) - math.ceil(number_skip/2) + 2:

        index_corrupted = math.ceil(number_skip / 2) + 1

        while index_corrupted <= len(array) - number_skip - 2:
            copy_array = array.copy()
            # The instruction to corrupt should be a 32-bit instruction
            if array[index_corrupted].find(',') > 0 and (useful_functions.is_16_bit(array[index_corrupted])==False):
                # Select the instructions to be skipped and those to be repeated
                list_index_skipped = useful_functions.select_instruction(array, number_skip + 1, index_corrupted + 1)

                if len(list_index_skipped) > number_skip:
                    index_last_skipped = list_index_skipped[len(list_index_skipped) - 1]
                    list_skipped = list_index_skipped[:len(list_index_skipped) - 1]
                    # The last instruction skipped should be a 32-bit instruction
                    if array[index_last_skipped].find(',') > 0 and useful_functions.is_16_bit(array[index_last_skipped])==False:

                        for number_repeat in range(math.ceil(number_skip / 2),min(number_skip * 2,index_corrupted) + 1):

                            list_index_repeated = useful_functions.select_instruction(array[:index_corrupted],
                                                                                      len(array[:index_corrupted]), 0)

                            if len(list_index_repeated) > number_repeat:

                                list_index_repeated = list_index_repeated[len(list_index_repeated) - number_repeat - 1:]
                                index_first_repeated = list_index_repeated[0]

                                list_index_repeated = list_index_repeated[1:]
                                # The last instruction skipped and the first repeated should be 32-bit instructions
                                if array[index_first_repeated].find(',') > 0 and (useful_functions.is_16_bit(array[index_first_repeated]))==False :
                                    # Getting the encoding of the three instructions
                                    encoding_corrupted = useful_functions.assembly_to_encoding(array[index_corrupted])
                                    encoding_first_repeated = useful_functions.assembly_to_encoding(array[index_first_repeated])
                                    encoding_last_skipped = useful_functions.assembly_to_encoding(array[index_last_skipped])

                                    # Corrupting the encoding of the two 32-bit instructions
                                    encoding_first_corrupted = encoding_corrupted[0:2] + encoding_first_repeated[2:4]
                                    encoding_second_corrupted = encoding_corrupted[0:2] + encoding_last_skipped[2:4]

                                    # Changing the corrupted instructions from encoding to arm instructions
                                    try:
                                        first_corrupted = useful_functions.encoding_to_assembly(encoding_first_corrupted)
                                        second_corrupted = useful_functions.encoding_to_assembly(encoding_second_corrupted)
                                        copy_array[index_corrupted] = first_corrupted
                                        min_of_indexes = min(number_skip, number_repeat)
                                        for index in range(min_of_indexes):
                                            copy_array[list_skipped[index]] = copy_array[
                                                list_index_repeated[index]]

                                        if len(list_index_repeated) < len(list_skipped):
                                            for index in range(min_of_indexes, len(list_skipped)):
                                                copy_array[list_skipped[index]] = "MOV(R0,R0)"

                                        elif len(list_index_repeated) > len(list_skipped):
                                            for index in range(min_of_indexes, len(list_index_repeated)):
                                                copy_array.insert(list_skipped[len(list_skipped) - 1] + 1,
                                                                  array[list_index_repeated[index]])

                                        copy_array[index_corrupted+max(number_skip,number_repeat)+1] = second_corrupted
                                        header = "CorruptSkipRepeat_" + str(number_skip) + "_" + str(index_corrupted) + "_" + str(number_repeat) + '_' + str(
                                            index_first_repeated) + "_" + str(index_last_skipped)

                                        # Updating the registers and the flags with their initial values
                                        registers.initialize()
                                        array_initialisation = useful_functions.file_to_array(
                                            'initialisation.txt')  # Creating a list of instructions
                                        useful_functions.execute_assembly(array_initialisation)  # Executing the instruction

                                        # Executing the new formed code
                                        copy_array = [each_string.upper() for each_string in copy_array]

                                        # Simulating the model for 5 seconds and if it did not finish yet then we assume it is an infinite loop
                                        signal.signal(signal.SIGALRM, useful_functions.handler)
                                        signal.alarm(1)
                                        try:
                                            print('--------', header)
                                            useful_functions.execute_assembly(copy_array)
                                            useful_functions.fault_simulation_output(header)

                                        except:
                                            header = "CrashInfiniteCorruptSkipRepeat_" + str(number_skip) + "_" + str(
                                                index_corrupted) + "_" + str(number_repeat) + '_' + str(index_first_repeated) + "_" + str(index_last_skipped)
                                            useful_functions.fault_simulation_output(header)

                                    except:
                                        header = "CrashCorruptSkipRepeat_" + str(number_skip) + "_" + str(
                                            index_corrupted) + "_" + str(index_first_repeated) + "_" + str(index_last_skipped)
                                        useful_functions.fault_simulation_output(header)
            index_corrupted = index_corrupted + 1
        number_skip = number_skip + 1


def corrupt_skip_repeat_16(array):
    number_skip = 0
    # The minimum number of instructions repeated is the half of the number of instructions skipped
    while number_skip <= len(array) - math.ceil(number_skip/2) + 2:

        index_corrupted = math.ceil(number_skip / 2) + 1

        while index_corrupted <= len(array) - number_skip - 2:
            copy_array = array.copy()
            # The instruction to corrupt should be a 32-bit instruction
            if array[index_corrupted].find(',') > 0 and (useful_functions.is_16_bit(array[index_corrupted])==False):
                # Select the instructions to be skipped and those to be repeated
                list_index_skipped = useful_functions.select_instruction(array, number_skip + 1, index_corrupted + 1)

                if len(list_index_skipped) > number_skip:
                    index_last_skipped = list_index_skipped[len(list_index_skipped) - 1]
                    list_skipped = list_index_skipped[:len(list_index_skipped) - 1]
                    # The last instruction skipped should be a 32-bit instruction
                    if array[index_last_skipped].find(',') > 0 and useful_functions.is_16_bit(array[index_last_skipped])==False:

                        for number_repeat in range(math.ceil(number_skip / 2),min(number_skip * 2,index_corrupted) + 1):

                            list_index_repeated = useful_functions.select_instruction(array[:index_corrupted],
                                                                                      len(array[:index_corrupted]), 0)

                            if len(list_index_repeated) > number_repeat:

                                list_index_repeated = list_index_repeated[len(list_index_repeated) - number_repeat - 1:]
                                index_first_repeated = list_index_repeated[0]

                                list_index_repeated = list_index_repeated[1:]
                                # The last instruction skipped and the first repeated should be 32-bit instructions
                                if array[index_first_repeated].find(',') > 0 and useful_functions.is_16_bit(array[index_first_repeated]):
                                    # Getting the encoding of the three instructions
                                    encoding_corrupted = useful_functions.assembly_to_encoding(array[index_corrupted])
                                    encoding_first_repeated = useful_functions.assembly_to_encoding(array[index_first_repeated])
                                    encoding_last_skipped = useful_functions.assembly_to_encoding(array[index_last_skipped])

                                    # Corrupting the encoding of the two 32-bit instructions
                                    encoding_first_corrupted = encoding_corrupted[0:2] + encoding_first_repeated
                                    encoding_second_corrupted = encoding_corrupted[0:2] + encoding_last_skipped[2:4]

                                    # Changing the corrupted instructions from encoding to arm instructions
                                    try:
                                        first_corrupted = useful_functions.encoding_to_assembly(encoding_first_corrupted)
                                        second_corrupted = useful_functions.encoding_to_assembly(encoding_second_corrupted)
                                        copy_array[index_corrupted] = first_corrupted
                                        min_of_indexes = min(number_skip, number_repeat)
                                        for index in range(min_of_indexes):
                                            copy_array[list_skipped[index]] = copy_array[
                                                list_index_repeated[index]]

                                        if len(list_index_repeated) < len(list_skipped):
                                            for index in range(min_of_indexes, len(list_skipped)):
                                                copy_array[list_skipped[index]] = "MOV(R0,R0)"

                                        elif len(list_index_repeated) > len(list_skipped):
                                            for index in range(min_of_indexes, len(list_index_repeated)):
                                                copy_array.insert(list_skipped[len(list_skipped) - 1] + 1,
                                                                  array[list_index_repeated[index]])

                                        copy_array[index_corrupted+max(number_skip,number_repeat)+1] = second_corrupted
                                        header = "CorruptSkipRepeat16_" + str(number_skip) + "_" + str(index_corrupted) + "_" + str(number_repeat) + '_' + str(
                                            index_first_repeated) + "_" + str(index_last_skipped)

                                        # Updating the registers and the flags with their initial values
                                        registers.initialize()
                                        array_initialisation = useful_functions.file_to_array(
                                            'initialisation.txt')  # Creating a list of instructions
                                        useful_functions.execute_assembly(array_initialisation)  # Executing the instruction

                                        # Executing the new formed code
                                        copy_array = [each_string.upper() for each_string in copy_array]

                                        # Simulating the model for 5 seconds and if it did not finish yet then we assume it is an infinite loop
                                        signal.signal(signal.SIGALRM, useful_functions.handler)
                                        signal.alarm(1)
                                        try:
                                            print('--------', header)
                                            useful_functions.execute_assembly(copy_array)
                                            useful_functions.fault_simulation_output(header)

                                        except:
                                            header = "CrashInfiniteCorruptSkipRepeat16_" + str(number_skip) + "_" + str(
                                                index_corrupted) + "_" + str(number_repeat) + '_' + str(index_first_repeated) + "_" + str(index_last_skipped)
                                            useful_functions.fault_simulation_output(header)

                                    except:
                                        header = "CrashCorruptSkipRepeat16_" + str(number_skip) + "_" + str(
                                            index_corrupted) + "_" + str(index_first_repeated) + "_" + str(index_last_skipped)
                                        useful_functions.fault_simulation_output(header)
            index_corrupted = index_corrupted + 1
        number_skip = number_skip + 1


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

            list_of_index_skipped = useful_functions.select_instruction(array, number_of_instructions_skipped,
                                                                        index_first_instruction_skipped)
            if len(list_of_index_skipped) == number_of_instructions_skipped:

                # The number of repeated instructions varies from the round of then number of skipped instructions div 2
                # and  minimum  between the number of instruction skipped multiplied by 2 and the number of
                # instructions already executed
                for number_of_instructions_repeated in range(math.ceil(number_of_instructions_skipped / 2),
                                                             min(number_of_instructions_skipped * 2,
                                                                 index_first_instruction_skipped) + 1):

                    for index_first_instruction_repeated in range(0, index_first_instruction_skipped -
                                                                     number_of_instructions_repeated):
                        list_of_index_repeated = useful_functions.select_instruction(array,
                                                                                     number_of_instructions_repeated,
                                                                                     index_first_instruction_repeated)
                        min_of_indexes = min(len(list_of_index_repeated), len(list_of_index_skipped))

                        if len(list_of_index_repeated) == number_of_instructions_repeated:
                            copy_lines = array.copy()

                            for index in range(min_of_indexes):
                                copy_lines[list_of_index_skipped[index]] = copy_lines[list_of_index_repeated[index]]

                            if len(list_of_index_repeated) < len(list_of_index_skipped):
                                for index in range(min_of_indexes, len(list_of_index_skipped)):
                                    copy_lines[list_of_index_skipped[index]] = "MOV(R0,R0)"

                            elif len(list_of_index_repeated) > len(list_of_index_skipped):
                                for index in range(min_of_indexes, len(list_of_index_repeated)):
                                    copy_lines.insert(list_of_index_skipped[len(list_of_index_skipped) - 1] + 1,
                                                      copy_lines[list_of_index_repeated[index]])

                            """ Updating the registers and the flags with their initial values"""
                            array_initialisation = useful_functions.file_to_array(
                                'initialisation.txt')  # Creating a list of instructions
                            useful_functions.execute_assembly(array_initialisation)  # Executing the instruction

                            signal.signal(signal.SIGALRM, useful_functions.handler)
                            signal.alarm(1)
                            try:
                                header = "NumInstrucskipped_" + str(
                                    number_of_instructions_skipped) + "_IndexFirstSkipped_" + str(
                                    index_first_instruction_skipped) + "_NumInstrucRep_" + str(
                                    number_of_instructions_repeated) + "_IndexFirstRep" + str(
                                    index_first_instruction_repeated)

                                print('--------------------\n', header)

                                """Executing the skip"""
                                useful_functions.execute_assembly(copy_lines)
                                useful_functions.fault_simulation_output(header)

                            except:
                                header = "CrashNumInstrucskipped_" + str(
                                    number_of_instructions_skipped) + "_IndexFirstSkipped_" + str(
                                    index_first_instruction_skipped) + "_NumInstrucRep_" + str(
                                    number_of_instructions_repeated) + "_IndexFirstRep" + str(
                                    index_first_instruction_repeated)
                                useful_functions.fault_simulation_output(header)
                                continue

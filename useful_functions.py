"""Some important functions are included in this file, which we will utilize in the main program."""
from ast import literal_eval
from assembly import *
import registers
from capstone import *
import pandas as pd


def file_to_array(file_path):
    """
        This function reads a file, divides it into lines, and returns the array of lines.

            Parameters:
                file_path (string) : The path of the file we want to divide

            Returns:
                (array) : An array containing the file's lines.
    """
    text_file = open(file_path, "r")
    lines = text_file.read().splitlines()
    lines = [each_string.upper() for each_string in lines]
    text_file.close()
    return lines


def get_arguments_of_function(assembly_code):
    """
        This function returns a list of arguments from the function assembly_code
            Parameters:
                assembly_code (string) : Presents a line of assembly code

            Returns:
                (list) : list of arguments

    """
    assembly_code = assembly_code.replace(" ", "")  # deleting the blank spaces in the string
    # Copying the arguments of the assembly function in a second string
    arguments = assembly_code[assembly_code.find('(') + 1:  assembly_code.find(')')]
    list_of_arguments = arguments.split(',')  # Creating an array of the assembly function arguments
    return list_of_arguments


def number_labels_in_list(array):
    """
        This function returns the number of labels in a list.
            :param array: list of assembly instructions
            :return: number of labels
    """
    count = 0
    for i in array:
        if i.find('(') < 0:
            count = count + 1
    return count


def update_assembly_code(assembly_code):
    """
        This function modifies the lines of the assembly code. In fact, we are going to update global values.
        To do so, a line of assembly code such as "add(R0,R0,R1)" should be modified in order to respect the global
        variables syntax and so presented like " registers.R0 = add ( registers.R0 , registers.R0 , registers.R1 ) " .

            Parameters:
                assembly_code (string) : Presents a line of assembly code

            Returns:
                (string) : An updates assembly code respecting the global variables syntax
    """
    if assembly_code.find(',') > 0:  # updating the assembly code except for branches

        list_of_arguments = get_arguments_of_function(
            assembly_code)  # Creating an array of the assembly function arguments

        for j in range(len(list_of_arguments)):
            if list_of_arguments[j].isnumeric():  # Verify if the argument is numeric, so we don't have to update it
                break
            else:  # If the argument is not numeric than it is a global variable, and so we have to replace its syntax
                list_of_arguments[j] = 'registers.' + list_of_arguments[j]

        # Updating the syntax
        updated_code = 'registers.' + assembly_code[assembly_code.find('(') + 1: assembly_code.find(',')] + ' = ' \
                       + assembly_code[:assembly_code.find('(')] + '(' + ",".join(list_of_arguments) + ')'

    elif assembly_code.find('(') > 0:  # If it is a branch syntax
        updated_code = assembly_code[:assembly_code.find('(')] + '("' + assembly_code[
                                                                        assembly_code.find('(') + 1: len(
                                                                            assembly_code) - 1] + '",array , i)'
    else:  # If it is a label we change nothing
        updated_code = assembly_code
    return updated_code


def changing_argument(corrupted, replacement):
    """
    This function is useful when corrupting an instruction.
    In fact, if the source operand of the corrupted function expects an immediate value and receives a register Rd,
    it would deal with it as if it was an immediate value equals d.
    And the opposite case, if it expects a register, but it gets an immediate value "d" then :
            - if the immediate values is superior to 15 : than the code would crash in the physical injection
              and will do nothing on a software simulation, so we can just ignore that case n our simulation.
            - if it is less than 15 then it would be changed to the register R"d" .

            :param corrupted: The corrupted operand
            :param replacement: The replacement operand
            :return: The new value of the corrupted operand
    """

    # If the operand of the corrupted instruction is an immediate value, while the new value is a register then the
    # index of the register will be considered as an immediate value
    if corrupted.isnumeric() and replacement.isnumeric() == False:
        replacement = replacement[1:]

    # If the operand of the corrupted instruction is a register, while the new value is an immediate value then the
    # immediate value, if it's less than 16, will be considered as the register index
    if corrupted.isnumeric() == False and replacement.isnumeric() and int(replacement) <= 15:
        replacement = "R" + str(replacement)
    return replacement


def assembly_to_encoding(assembly):
    """
    This function changes an assembly instruction to its encoding
    :param assembly: an assembly instruction
    :return: encoding of assembly instruction
    """
    import keystone as ks

    # Some add/sub instructions, when all the operands are registers and the first source operand is identical to the
    # destination operand they are considered in python as 16-bit instruction , so we have to modify them adding ".w'
    # to the opcode. Here I didn't check if the registers are identical because the add and sub instructions are 32
    # bit instructions in all cases.
    if assembly.find('ADD(') >= 0:
        ARM_CODE = assembly.replace('ADD(', 'add.w ')
        ARM_CODE = ARM_CODE.replace(')', ' ')
    elif assembly.find('SUB(') >= 0:
        ARM_CODE = assembly.replace('SUB(', 'sub.w ')
        ARM_CODE = ARM_CODE.replace(')', ' ')
    else:
        ARM_CODE = assembly.replace('(', ' ')
        ARM_CODE = ARM_CODE.replace(')', ' ')

    # initialize the keystone object with the ARM architecture
    ks = ks.Ks(ks.KS_ARCH_ARM, ks.KS_MODE_THUMB + ks.KS_MODE_BIG_ENDIAN)
    # Assemble the ARM code
    ARM_BYTECODE, _ = ks.asm(ARM_CODE)
    # convert the array of integers into bytes
    ARM_BYTECODE = bytes(ARM_BYTECODE)
    return ARM_BYTECODE


def is_16_bit(assembly):
    """
    This function checks if the assembly instruction is a 16-bit instruction
    :param assembly: assembly instruction
    :return: True if the assembly instruction is a 16-bit instruction, False otherwise
    """
    ARM_BYTECODE = assembly_to_encoding(assembly)
    return len(ARM_BYTECODE) == 2


def encoding_to_assembly(ARM_BYTECODE):
    """
    This function changes an encoding to its assembly instruction
    :param ARM_BYTECODE: encoding of an instruction
    :return: assembly instruction that corresponds to the bytecode
    """
    # Initialize the ARM disassembler in thumb big endian mode
    md = Cs(CS_ARCH_ARM, CS_MODE_BIG_ENDIAN + CS_MODE_THUMB)
    # iterate over each instruction and print it
    for j in md.disasm(ARM_BYTECODE, 0x1000):
        # Extracting the operands
        argument = j.op_str.split(',')
        # If the second source operand is in the format "0x." then we should convert it to decimal format
        if argument[0] == 'pc':
            argument[0] = 'r15'
        elif argument[0] == 'fp':
            argument[0] = 'r11'
        elif argument[0] == 'sl':
            argument[0] = 'r10'
        elif argument[0] == 'ip':
            argument[0] = 'r12'
        elif argument[0] == 'sb':
            argument[0] = 'r9'
        elif argument[0] == 'sp':
            argument[0] = 'r13'
        elif argument[0] == 'lr':
            argument[0] = 'r14'

        if argument[2].find('0x') > 0:
            argument[2] = str(int(argument[2][2:], 16))
        # If the second source operand is in the format "#." then it is an integer we have to just delete the symbol
        elif argument[2].find('#') > 0:
            argument[2] = (argument[2][2:])
        # The only case left, when it is a register we onl delete the extra space and if the register has a name then we
        # convert it to R...
        else:
            argument[2] = (argument[2][1:])
            if argument[2] == 'pc':
                argument[2] = 'r15'
            elif argument[2] == 'fp':
                argument[2] = 'r11'
            elif argument[2] == 'sl':
                argument[2] = 'r10'
            elif argument[2] == 'ip':
                argument[2] = 'r12'
            elif argument[2] == 'sb':
                argument[2] = 'r9'
            elif argument[2] == 'sp':
                argument[2] = 'r13'
            elif argument[2] == 'lr':
                argument[2] = 'r14'
        # We extract the opcode
        opcode = j.mnemonic
        # Reformatting the code in the appropriate syntaxe
        if opcode.find('.w') >= 0:
            opcode = opcode.replace('.w', '')
        arm_code = opcode + '(' + ",".join(argument) + ')'
        return arm_code


def select_instruction(array, number, index):
    """
    This function selects a number of instructions from the list "array" starting from specific index. This group of
    instructions should not contain a label.
    :param array: array containing assembly instructions
    :param number: number of instructions that should be returned
    :param index: index of the first index we start searching from
    :return: list of indexes
    """
    count = 1
    list_of_index = []
    while count <= number and index < len(array):
        if array[index].find('(') < 0:
            index = index + 1
        else:
            list_of_index.append(index)
            index = index + 1
            count = count + 1
    return list_of_index


def handler(signum, frame):
    """This fuction breaks the infinite loops"""
    raise Exception("end of time")


def execute_assembly(array):
    """
            This function runs the assembly code contained in an array and appends the output to a csv file with
            the header "header".

            Parameters:
                array (string) : An array of Assembly instructions
    """

    array = [each_string.upper() for each_string in array]

    i = 0
    while i < len(array):
        if array[i].find('(') < 0:  # If the code is a label we do nothing
            i = i + 1

        elif array[i].find(',') > 0:  # If the code is an assembly code but not a branch we execute it and increment i.
            exec(update_assembly_code(array[i]))
            i = i + 1

        elif array[i].find(',') < 0 and array[i].find('(') > 0:
            i = eval(update_assembly_code(array[i]))  # If the code is a branch, i will become the index of the label


def fault_simulation_output(header):
    # Creating a list that will contain the registers
    l = []
    # Initialize the registers and put them in an array
    if header.find('Crash') < 0:
        for i in range(13):
            l.append(str(eval("registers.R{}".format(i))))
    else:
        for i in range(13):
            l.append('?')
    # Creating the csv file
    try:
        df = pd.read_csv('output.csv')
    except:
        df = pd.DataFrame()

    # Adding the output to the csv file
    df[header] = l
    df.to_csv('output.csv', mode='w', index=False)

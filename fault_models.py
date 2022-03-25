import useful_functions


def skip(lines):
    """
        This function executes the skip fault model.

            :parameter :
                lines (array) : an array of assembly code

    """
    for j in range(min(9, len(lines))):  # The number of instructions that will be skipped
        for i in range(len(lines)):  # The index of the first instruction that will be skipped

            # Copying the original code in another list so that we don't lose the initial instructions
            copy_lines = lines.copy()

            # Exiting the code if he number of the instructions left is less than the number of instructions that
            # should be skipped
            if i == (len(lines) - j + 1):
                break
            else:
                for k in range(j):
                    copy_lines[i + k] = "mov(R0,R0)"  # Skipping j instructions
                    # The header will be in format skip_NumberOfInstructionsSkipped_IndexOfFirstInstructionSkipped
                    header = 'skip_' + str(k + 1) + '_' + str(i + 1)

                    """ Updating the registers with their initial values"""
                    array_initialisation = useful_functions.file_to_array(
                        'initialisation.txt')  # Creating a list of instructions from the file of initialization.
                    useful_functions.execute_assembly(array_initialisation, 'initial')

                    """Executing the skip"""
                    useful_functions.execute_assembly(copy_lines, header)


def skip_and_repeat(lines):
    """
        This function executes the skip and repeat fault model.

            :parameter :
                lines (array) : an array of assembly code

    """
    for i in range(len(lines)):   # The index of the instruction skipped

        # Copying the original code in another list so that we don't lose the initial instructions
        copy_lines = lines.copy()

        for j in range(0, i):  # The index of the instruction repeated
            copy_lines[i] = lines[j]  # Repeating the instruction j

            # The header will be in format Skip_IndexOfInstructionSkipped_Repeat_IndexOfInstructionRepeated
            header = "Skip_" + str(i+1) + "_Repeat_" + str(j+1)

            """ Updating the registers with their initial values"""
            array_initialisation = useful_functions.file_to_array(
                'initialisation.txt')  # Creating a list of instructions from the file of initialization.
            useful_functions.execute_assembly(array_initialisation, 'initial')

            """Executing the skip"""
            useful_functions.execute_assembly(copy_lines, header)


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

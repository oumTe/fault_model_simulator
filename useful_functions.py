"""Some important functions are included in this file, which we will utilize in the main program."""

from assembly import *
import registers
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


def execute_assembly(array):
    """
            This function runs the assembly code contained in an array and appends the output to a csv file with
            the header "header".

            Parameters:
                array (string) : An array of Assembly instructions
    """

    i = 0
    while i < len(array):
        if array[i].find('(') < 0:  # If the code is a label we do nothing
            i = i + 1

        elif array[i].find(',') > 0:  # If the code is an assembly code but not a branch we execute it and increment i.
            print(update_assembly_code(array[i]))
            exec(update_assembly_code(array[i]))
            i = i + 1

        elif array[i].find(',') < 0 and array[i].find('(') > 0:
            i = eval(update_assembly_code(array[i]))  # If the code is a branch, i will become the index of the label


def fault_simulation_output(header):
    # Creating a list that will contain the registers
    l = []
    # Initialize the registers and put them in an array
    for i in range(13):
        l.append(str(eval("registers.R{}".format(i))))

    # Creating the csv file
    try:
        df = pd.read_csv('output.csv')
    except:
        df = pd.DataFrame()

    # Adding the output to the csv file
    df[header] = l
    df.to_csv('output.csv', mode='w', index=False)


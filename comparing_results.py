import pandas as pd
import numpy as np


def comparing_results():
    """
        This function compares the result contained in two files : the fault models outputs and the fault injection
        output, and returns a list with the fault models that have probably occurred due to the fault injection.
    """
    fault = pd.read_csv('fault.csv')
    delay_row = fault.index[13]
    fault = fault.T.sort_values(by=delay_row).T
    unique_elements, counts_elements = np.unique(fault.iloc[13, :], return_counts=True)
    index = 0
    while index < fault.shape[1]:
        for i in range(len(unique_elements)):
            count = 0
            text_file = open("result.txt", "a")
            text_file.write('--------------------- Delay = {} \n'.format(unique_elements[i]))
            number_of_experiences = input("Please enter the number of experiences at this delay: ")
            for j in range(counts_elements[i]):
                count = count + fault.loc[14][index]
                text_file.close()
                comparing_results_by_line(fault.iloc[:, index], int(number_of_experiences))
                index = index + 1
                count = int(number_of_experiences) - count
            text_file = open("result.txt", "a")
            text_file.write('Crashes at delay = {} equals {} \n'.format(unique_elements[i] , count))


def comparing_results_by_line(line,number_of_experiences):
    """
        This function compares with one line of the file containing faulty behaviour
    """
    models = pd.read_csv('output.csv')  # Reading the file containing the output of different fault models
    result = []  # Initialize the list that will have the software models with similar results as the fault injection
    for i in range(models.shape[1]):  # Reading the fault models file by column
        """
            A Boolean variable that will be comparing two columns of the list and becomes false as soon as it finds 
            a different cell.
        """
        boolean = True
        j = 0  # Counter that reads the file rows
        """
            Setting out condition for the comparison, if we find a different cell or if j exceeds the number of rows
        """
        while boolean and j < models.shape[0]:
            boolean = (models.iloc[:, i][j] == line[j])  # The boolean if set to false if the cells are different
            j += 1  # We increase our counter
        """ 
            If the variable boolean is true then we append to the list the name of this column which is the fault 
            model that occurred
        """
        if boolean:
            result.append(models.iloc[:, i].name)
    text_file = open("result.txt", "a")

    text_file.write('The output of the physical injection is : {} \n'.format(line.to_list()))
    if len(result) == 0:
        text_file.write('Model Name : This is an unknown model \n')
    else:
        name = ''
        for i in range(len(result)):
            name = changing_name(result[i])
        text_file.write(name)
    text_file.write('This model was observed {} % of times \n'.format(line[14] * 100 / number_of_experiences))


def changing_name(name):
    if name == 'Golden':
        name = 'Model Name : Silent case'
    elif name.find('skip_') >= 0:
        name_split = name.split('_')
        number_of_instruction_skipped = name_split[1]
        index_first_instruction_skipped = name_split[2]
        name = 'Model Name : Skip. \nNumber of skipped instructions = ' + number_of_instruction_skipped + \
               '\nIndex of first instruction Skipped = ' + index_first_instruction_skipped

    elif name.find('SingleInstructionCorruption') >= 0:
        name_split = name.split('_')
        name = "Model Name : One instruction Corruption model while skipping the next instruction. \n" + \
               "Index of skipped instruction = " + name_split[1] + \
               "\nThe destination operand and the second source operand of the instruction number " + \
               str(int(name_split[1]) - 1) + " are replaced with those of the skipped instruction"
    elif name.find("TwoInstructionsCorruption") >= 0 :
        name_split = name.split('_')
        index_first_corrupted = name_split[1]
        name = "Model Name : Two Instructions Corruption. \nChanging the destination and second source operands of the "+ \
                "instruction number " + index_first_corrupted + " with those of the instruction number " + \
                str(int(index_first_corrupted) + 1) + "\nChanging the opcode and the first source operand of" + \
                "instruction number "  + name_split[3] + " with those of the instruction number " + index_first_corrupted
    return name

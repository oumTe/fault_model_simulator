import pandas as pd
import numpy as np
from fpdf import FPDF


def comparing_results():
    """
        This function compares the result contained in two files : the fault models outputs and the fault injection
        output, and returns a list with the fault models that have probably occurred due to the fault injection.
    """
    fault = pd.read_csv('fault.csv')  # Reading the file containing the fault injection outcomes
    delay_row = fault.index[13]  # Extracting the row containing the delay
    fault = fault.T.sort_values(by=delay_row).T  # Sorting the fault injection outcomes by delay
    unique_elements, counts_elements = np.unique(fault.iloc[13, :], return_counts=True)  # Counting the occurrence of
    # each unique delay
    index = 0
    number_of_experiences = input("Please enter the number of experiences: ")  # Asking the user to provide the
    # number of experiments
    pdf = FPDF()
    pdf.add_page()
    while index < fault.shape[1]:  # Comparing each column of the fault injection CSV file with the output of the
        # fault simulation
        for i in range(len(unique_elements)):  # Grouping the results by delay
            crashes = 0  # This variable counts the number of crashes at a specific delay

            pdf.set_font("Arial", 'B',  size=42)
            pdf.set_text_color(143,221,231)
            pdf.cell(195, 40 , txt='Delay : {}'.format(unique_elements[i]),ln=1, align='C')


            #  Browsing the fault injection outcomes columns for that specific delay
            for j in range(counts_elements[i]):

                crashes = crashes + fault.loc[14][index]  # Incrementing the crashes variable with the number of times the
                # model was observed
                comparing_results_by_line(fault.iloc[:, index], int(number_of_experiences) , pdf) # Comparing each column
                # with the simulation results
                index = index + 1
                crashes = int(number_of_experiences) - crashes # The number of crushes is the total number of
                # experiences minus the numer of observed models

            # number of crashes at this delay
            pdf.set_font("Arial", 'I')
            pdf.set_text_color(239, 124, 142)
            pdf.cell(195, 15, 'Crashes at delay = {} equals {}'.format(unique_elements[i], crashes),0, 1, '')



    pdf.output("report.pdf")


def comparing_results_by_line(line, number_of_experiences , pdf):
    """
        This function compares with one line of the file containing faulty behaviour
    """
    models = pd.read_csv('output.csv')  # Reading the file containing the output of the fault simulation
    result = []  # Initialize the list that will have the software models with similar results as the fault injection
    for i in range(models.shape[1]):  # Reading the fault models simulation outcomes file by column
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
        if boolean:  # If the fault injection outcome matches the model we add the model name to the list
            result.append(models.iloc[:, i].name)

    # Writing the fault injection outcome to the report
    pdf.set_font("Arial", 'B' , size=15)
    pdf.set_text_color(239, 124, 142)
    pdf.multi_cell(195, 10, 'The output of the physical injection is :', 0, 1, '')

    pdf.set_font("Arial", size=12)
    pdf.set_text_color(0, 0, 0)
    pdf.multi_cell(195, 5, '{}'.format(line.to_list()), 0, 1, '')

    if len(result) == 0:  # If the array is empty then, there is no matched model : this is considered as an unknown
        # model
        pdf.cell(60, 5 ,'   This is an unknown model !', 0, 1, '')
    else:
        name = ''

        # possible software models that matches with the fault injection
        pdf.set_font("Arial", 'U', size=15)
        pdf.set_text_color(255, 194, 199)
        pdf.cell(195, 15, 'There are {} possible models for this case:'.format(len(result)), 0, 1, '')

        for i in range(len(result)):
            pdf.set_font("Arial", 'B' , 15)
            pdf.set_text_color(182, 229, 216)
            pdf.cell(195, 10, '* Model Number {} :'.format(i + 1), 0, 1, '')

            name = changing_name(result[i])  # Changing the SW model name from the one provided by the python code to
            # a more detailed one
            pdf.set_font("Arial", size=12)
            pdf.set_text_color(0, 0, 0)
            pdf.multi_cell(195, 5, name , 0, 1, '')

    # We print the percent of times these models was observes
    pdf.set_font("Arial", 'B', size=12)
    pdf.set_text_color(127, 143, 163)
    pdf.cell(195, 15, '\n ====> This model was observed {} % of times \n'.format(line[14] * 100 / number_of_experiences), 0, 1, '')


def changing_name(name):
    """
    This function aims to change the model name provided automatically by python to a more detailed one
    :param name: the default name generated by python
    :return: The new model name and its description
    """
    if name == 'Golden':
        name = '        This is a SILENT case'

    elif name.find('skip_') >= 0:
        name_split = name.split('_')
        number_of_instruction_skipped = name_split[1]
        index_first_instruction_skipped = name_split[2]
        name = 'Model Name : Skip Model.\n      Number of skipped instructions = ' + number_of_instruction_skipped + \
               '\n      Index of first instruction Skipped = ' + index_first_instruction_skipped

    elif name.find('SingleInstructionCorruption') >= 0:
        name_split = name.split('_')
        name = "Model Name : One instruction Corruption model while skipping the next instruction." + \
               "\n      Index of skipped instruction = " + name_split[1] + \
               "\n      The destination operand and the second source operand of the instruction number " + \
               str(int(name_split[1]) - 1) + " are replaced with those of the skipped instruction"

    elif name.find("TwoInstructionsCorruption") >= 0:
        name_split = name.split('_')
        index_first_corrupted = name_split[1]
        name = "Model Name : Two Instructions Corruption.\n       Changing the destination and second  " + \
               "source operands of the instruction number " + index_first_corrupted + " with those of the instruction number " + \
               str(int(index_first_corrupted) + 1) + "\n       Changing the opcode and the first source operand of " + \
               "instruction number " + name_split[3] + " with those of the instruction number " + index_first_corrupted

    elif name.find("NumInstrucskipped") >= 0:
        name_split = name.split('_')
        name = "Model Name : Skip and Repeat.\n     Number of instructions Skipped: " + name_split[1] + \
               "\n     Index of first instruction skipped : " + name_split[3] + \
               "\n     Number of instruction Repeated : " + name_split[5] + \
               "\n     Index of first instruction repeated : " + name_split[7]

    elif name.find("DestinationOperandCorruption") >= 0:
        name_split = name.split('_')
        name = "Model Name : Destination Operand Replacement.\nIn this model we corrupt the destination operand " + \
               "with the one of the previous instruction." + \
               "\n     Index of Corrupted Instruction : " + name_split[1]

    elif name.find("FirstSourceOperandCorruption") >= 0:
        name_split = name.split('_')
        name = "Model Name : First Source Operand Replacement.\nIn this model we corrupt the first source operand " + \
               "with the one of the previous instruction." + \
               "\n     Index of Corrupted Instruction : " + name_split[1]

    elif name.find("SecondSourceOperandCorruption") >= 0:
        name_split = name.split('_')
        if name_split[0] == "1":
            name = "Model Name : Source Operand Replacement.\nIn this model we corrupt the source operand " \
               + "with the second source operand of the previous instruction." + \
               "\n     Index of Corrupted Instruction : " + name_split[1]
            print('-----------------------------------------------------',name)
        else:
            name = "Model Name : Second source Operand Replacement.\nIn this model we corrupt the second source  " \
               + "operand with the one of the previous instruction." + \
               "\n     Index of Corrupted Instruction : " + name_split[1]
    elif name.find("Skipping_") >= 0 :
        name_split = name.split('_')
        name  = "Model Name : Instruction Skip and new instruction execution. " \
            + "\n     In this model we skipped " + name_split[1] + " instruction(s) and executed the " + \
            "instruction formed with the least 16 bits of the instruction " + str(int(name_split[1]) - 1) + "."
    return name

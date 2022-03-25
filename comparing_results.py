import pandas as pd


def comparing_results():
    """
        This function compares the result contained in two files : the fault models outputs and the fault injection
        output, and returns a list with the fault models that have probably occurred due to the fault injection.
    """
    models = pd.read_csv('output.csv')  # Reading the file containing the output of different fault models
    fault = pd.read_csv('convertcsv.csv')  # Reading the file containing the output of the fault injection
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
            boolean = (models.iloc[:, i][j] == fault.iloc[:, 0][
                j])  # The boolean if set to false if the cells are different
            j += 1  # We increase our counter
        """ 
            If the variable boolean is true then we append to the list the name of this column which is the fault 
            model that occurred
        """
        if boolean:
            result.append(models.iloc[:, i].name)
    print(result)

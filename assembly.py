# This file contains the definition of some assembly functions

def mov(r, n):
    """
        Stores in the register r the value of and returns the new value of the register.

            Parameters:
                r (int) : one of the global values presenting the registers
                n (int) : the new value of the register

            Returns:
                (int) : the new value stored in the register r
    """
    r = n
    return r


def movw(r, n):
    """ Stores in the register r the value of and prints the new value of the register.

            Parameters:
                r (int) : one of the global values presenting the registers
                n (int) : the new value of the register ,We may use one of the global variables (register)
    """
    r = n
    print(r)


def add(r, Rn, n):
    """ Stores in the register r the result of adding the value of Rn and n.

            Parameters:
                r (int) : one of the global values presenting the registers
                Rn (int) : one of the global values presenting the registers
                n (int) : the value that will e added to Rn,We may use one of the global variables (register)

            Returns:
                (int) : the new value stored in the register r

    """
    r = Rn + n
    return r

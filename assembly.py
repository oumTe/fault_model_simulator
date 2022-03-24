# This file contains the definition of some assembly functions
import ctypes

"""Register move instructions"""


def mov(Rd, n):
    """
        Writes to Rd the value of n which could be an ARM register or an 8-bit immediate value.

            Parameters:
                Rd (register) : The destination ARM register
                n (int) :  8-bit immediate value or ARM register

            Returns:
                (int) : The new value stored in the register Rd
    """
    Rd = n
    return Rd


def movw(Rd, imm16):
    """
        Writes a 16-bit immediate value to Rd.

            Parameters:
                Rd (register) : The destination ARM register
                imm16 (int) :  16-bit immediate value

            Returns:
                (int) : The new value stored in the register Rd
    """
    Rd = imm16
    return Rd


def movt(Rd, imm16):
    """
        Writes a 16-bit immediate value to the top half-word of a register, without affecting the bottom half-word.

            Parameters:
                Rd (register) : The destination ARM register
                imm16 (int) :  16-bit immediate value

            Returns:
                (int) : The new value stored in the register Rd
    """
    Rd = (Rd & 0xffff) | (imm16 << 16)
    return Rd


def movwt(Rd, imm32):
    """
        Writes a 32-bit immediate value to Rd.

            Parameters:
                Rd (register) : The destination ARM register
                imm32 (int) :  32-bit immediate value

            Returns:
                (int) : The new value stored in the register Rd
    """
    Rd = imm32
    return Rd


######################################################################################################################

"""Load register from memory"""


def ldr(Rt, Rn, imm7):
    """
        Load the register Rt from a 32-bit word contained in the memory address obtained by adding Rn et the 7-bit
        immediate value  imm7.

            Parameters:
                Rt (register) : The destination ARM register
                Rn (register) : An ARM register
                imm7 (int) :  7-bit immediate value

            Returns:
                (int) : The new value stored in the register Rt
    """
    address = Rn + imm7
    Rd = ctypes.cast(address, ctypes.py_object).value
    return Rt


def ldrb(Rt, Rn, imm5):
    """
        Load the register Rt from a byte contained in the memory address obtained by adding Rn et the 7-bit
        immediate value  imm7.

            Parameters:
                Rt (register) : The destination ARM register
                Rn (register) : An ARM register
                imm5 (int) :  5-bit immediate value

            Returns:
                (int) : The new value stored in the register Rt
    """
    address = Rn + imm5
    Rd = ctypes.cast(address, ctypes.py_object).value
    return Rt


def ldrh(Rt, Rn, imm6):
    """
        Load the register Rt from a 16-bit half-word contained in the memory address obtained by adding Rn et the 7-bit
        immediate value  imm7.

            Parameters:
                Rt (register) : The destination ARM register
                Rn (register) : An ARM register
                imm6 (int) :  6-bit immediate value

            Returns:
                (int) : The new value stored in the register Rt
    """
    address = Rn + imm6
    Rd = ctypes.cast(address, ctypes.py_object).value
    return Rt


######################################################################################################################
"""Arithmetic instructions"""


def add(Rd, Rn, n):
    """ Writes to the register Rd the result obtained by adding the immediate value or the register n to the register Rn

            Parameters:
                Rd (register) : The destination ARM register
                Rn (register) : An ARM register
                n (int) :  immediate value or ARM register

            Returns:
                (int) : The new value stored in the register Rd

    """
    Rd = Rn + n
    return Rd


def sub(Rd, Rn, n):
    """ Writes to the register Rd the result obtained by subtracting the immediate value or the register n from
        the register Rn

            Parameters:
                Rd (register) : The destination ARM register
                Rn (register) : An ARM register
                n (int) :  immediate value or ARM register

            Returns:
                (int) : The new value stored in the register Rd

    """
    Rd = Rn - n
    return Rd


def neg(Rd, Rn):
    """ Writes to the register Rd the negation of the register Rn

            Parameters:
                Rd (register) : The destination ARM register
                Rn (register) : An ARM register

            Returns:
                (int) : The new value stored in the register Rd

    """
    Rd = -Rn
    return Rd


def mul(Rd, Rn):
    """ Writes to the register Rd the result obtained by multiplying the register Rd by the register Rn
            Parameters:
                Rd (register) : The destination ARM register
                Rn (register) : An ARM register

            Returns:
                (int) : The new value stored in the register Rd

    """
    Rd = Rd * Rn
    return Rd


def sdiv(Rd, Rn, Rm):
    """ Writes to the register Rd the result obtained after a signed division of the register Rn by the register Rm.

            Parameters:
                Rd (register) : The destination ARM register
                Rn (register) : An ARM register
                Rm (register) : An ARM register

            Returns:
                (int) : The new value stored in the register Rd

    """
    Rd = Rn / Rm
    return Rd


def udiv(Rd, Rn, Rm):
    """ Writes to the register Rd the result obtained after an unsigned division of the register Rn by the register Rm.

            Parameters:
                Rd (register) : The destination ARM register
                Rn (register) : An ARM register
                Rm (register) : An ARM register

            Returns:
                (int) : The new value stored in the register Rd

    """
    Rd = Rn / Rm
    return Rd


######################################################################################################################
"""Logical instructions"""


def and_(Rd, Rn):
    """ Writes to the register Rd the result obtained after performing a bitwise AND between Rd and Rn.

            Parameters:
                Rd (register) : The destination ARM register
                Rn (register) : An ARM register

            Returns:
                (int) : The new value stored in the register Rd

    """
    Rd &= Rn
    return Rd


def orr(Rd, Rn):
    """ Writes to the register Rd the result obtained after performing a bitwise OR between Rd and Rn.

            Parameters:
                Rd (register) : The destination ARM register
                Rn (register) : An ARM register

            Returns:
                (int) : The new value stored in the register Rd

    """
    Rd |= Rn
    return Rd


def ero(Rd, Rn):
    """ Writes to the register Rd the result obtained after performing a bitwise XOR between Rd and Rn.

            Parameters:
                Rd (register) : The destination ARM register
                Rn (register) : An ARM register

            Returns:
                (int) : The new value stored in the register Rd

    """
    Rd ^= Rn
    return Rd


def mvn(Rd, Rn):
    """ Writes to the register Rd the r 1’s complement of Rn.

            Parameters:
                Rd (register) : The destination ARM register
                Rn (register) : An ARM register

            Returns:
                (int) : The new value stored in the register Rd

    """
    Rd = Rn ^ 0xffffffff
    return Rd


def bic(Rd, Rn):
    """  Bit clear Rd using mask in Rn.

            Parameters:
                Rd (register) : The destination ARM register
                Rn (register) : An ARM register

            Returns:
                (int) : The new value stored in the register Rd

    """
    Rd &= ~Rn
    return Rd


######################################################################################################################
"""Shift and rotation instructions"""


def lsl(Rd, Rn):
    """  Writes to Rd the result of left shifting Rn.

            Parameters:
                Rd (register) : The destination ARM register
                Rn (register) : An ARM register

            Returns:
                (int) : The new value stored in the register Rd

    """
    Rd <<= Rn
    return Rd


def lsl(Rd, Rn):
    """  Writes to Rd the result of logical right-shifting Rn.

            Parameters:
                Rd (register) : The destination ARM register
                Rn (register) : An ARM register

            Returns:
                (int) : The new value stored in the register Rd

    """
    Rd = (Rd & 0xffffffff) >> Rn
    return Rd


def asr(Rd, Rn):
    """  Writes to Rd the result of arithmetic right-shifting Rn.

            Parameters:
                Rd (register) : The destination ARM register
                Rn (register) : An ARM register

            Returns:
                (int) : The new value stored in the register Rd

    """
    Rd >>= Rn
    return Rd



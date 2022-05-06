# This file contains the definition of some assembly functions
import ctypes
import registers
import numpy as np

"""Register move instructions"""


def mov(Rd, n):
    """
        Writes to Rd the value of n which could be an ARM register or an 8-bit immediate value.

            Parameters:
                Rd (register) : The destination ARM register
                n (int) :  8-bit immediate value or ARM register

    """
    Rd = n
    Rd = np.uint32(Rd)
    return Rd


def movw(Rd, imm16):
    """
        Writes a 16-bit immediate value to Rd.

            Parameters:
                Rd (register) : The destination ARM register
                imm16 (int) :  16-bit immediate value

    """
    Rd = imm16
    Rd = np.uint32(Rd)
    return Rd


def movt(Rd, imm16):
    """
        Writes a 16-bit immediate value to the top half-word of a register, without affecting the bottom half-word.

            Parameters:
                Rd (register) : The destination ARM register
                imm16 (int) :  16-bit immediate value

    """
    Rd = (Rd & 0xffff) | (imm16 << 16)
    Rd = np.uint32(Rd)
    return Rd


def movwt(Rd, imm32):
    """
        Writes a 32-bit immediate value to Rd.

            Parameters:
                Rd (register) : The destination ARM register
                imm32 (int) :  32-bit immediate value


    """
    Rd = imm32
    Rd = np.uint32(Rd)
    return Rd


######################################################################################################################

"""Load register from memory"""


def ldr(Rt, Rn, imm7):
    """
        Load the register Rt from a 32-bit word contained in the memory address obtained by adding Rn and the 7-bit
        immediate value  imm7.

            Parameters:
                Rt (register) : The destination ARM register
                Rn (register) : An ARM register
                imm7 (int) :  7-bit immediate value

    """
    address = Rn + imm7
    Rt = registers.memory[address]
    Rt = np.uint32(Rt)
    return Rt


def ldrb(Rt, Rn, imm5):
    """
        Load the register Rt from a byte contained in the memory address obtained by adding Rn and the 5-bit
        immediate value imm5.

            Parameters:
                Rt (register) : The destination ARM register
                Rn (register) : An ARM register
                imm5 (int) :  5-bit immediate value

    """
    address = Rn + imm5
    Rt = registers.memory[address]
    Rt = np.uint32(Rt)
    return Rt


def ldrh(Rt, Rn, imm6):
    """
        Load the register Rt from a 16-bit half-word contained in the memory address obtained by adding Rn and the 6-bit
        immediate value  imm6.

            Parameters:
                Rt (register) : The destination ARM register
                Rn (register) : An ARM register
                imm6 (int) :  6-bit immediate value

    """
    address = Rn + imm6
    Rt = registers.memory[address]
    Rt = np.uint32(Rt)
    return Rt


######################################################################################################################

"""Store register to memory"""


def str_(Rt, Rn, imm7):
    """
        Stores the value of the register Rt to the memory address obtained by adding Rn to the 7-bit
        immediate value  imm7.

            Parameters:
                Rt (register) : The destination ARM register
                Rn (register) : An ARM register
                imm7 (int) :  7-bit immediate value

            Returns:
                (int) : The new value stored in the register Rt
    """
    address = Rn + imm7
    registers.memory[address] = Rt
    return registers.memory[address]


def ldrb(Rt, Rn, imm5):
    """
        Stores the value of the register Rt to the memory address obtained by adding Rn to the 5-bit
        immediate value  imm5.

            Parameters:
                Rt (register) : The destination ARM register
                Rn (register) : An ARM register
                imm5 (int) :  5-bit immediate value

            Returns:
                (int) : The new value stored in the register Rt
    """
    address = Rn + imm5
    Rt = registers.memory[address]
    return registers.memory[address]


def ldrh(Rt, Rn, imm6):
    """
        Stores the value of the register Rt to the memory address obtained by adding Rn to the 6-bit
        immediate value  imm6.

            Parameters:
                Rt (register) : The destination ARM register
                Rn (register) : An ARM register
                imm6 (int) :  6-bit immediate value

            Returns:
                (int) : The new value stored in the register Rt
    """
    address = Rn + imm6
    Rt = registers.memory[address]
    return registers.memory[address]


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


def lsl(Rd, Rn, imm):
    """  Writes to Rd the result of left shifting Rn by imm bits.

            Parameters:
                Rd (register) : The destination ARM register
                Rn (register) : An ARM register
                imm (int) : immediate value, number of bits shifted

            Returns:
                (int) : The new value stored in the register Rd

    """
    Rd = Rn << imm
    Rd = np.uint32(Rd)
    return Rd


def lsls(Rd, Rn, imm):
    """  Writes to Rd the result of logical right-shifting Rn by imm bits.

            Parameters:
                Rd (register) : The destination ARM register
                Rn (register) : An ARM register
                imm (int) : immediate value, number of bits shifted

            Returns:
                (int) : The new value stored in the register Rd

    """
    Rd = (Rn & 0xffffffff) >> imm
    return Rd


def asr(Rd, Rn, imm):
    """  Writes to Rd the result of arithmetic right-shifting Rn byimm bits.

            Parameters:
                Rd (register) : The destination ARM register
                Rn (register) : An ARM register
                imm (int) : immediate value, number of bits shifted

            Returns:
                (int) : The new value stored in the register Rd

    """
    Rd = Rn >> imm
    return Rd


def ror(Rd, Rn, imm):
    """  Writes to Rd the result of right rotating Rn by imm bits.

            Parameters:
                Rd (register) : The destination ARM register
                Rn (register) : An ARM register
                imm (int) : immediate value, number of bits rotated

            Returns:
                (int) : The new value stored in the register Rd

    """
    Rd = (Rn >> imm) | (Rn << (32 - imm)) & 0xFFFFFFFF
    return Rd


def rol(Rd, Rn, imm):
    """  Writes to Rd the result of left rotating Rn by imm bits.

            Parameters:
                Rd (register) : The destination ARM register
                Rn (register) : An ARM register
                imm (int) : immediate value, number of bits rotated

            Returns:
                (int) : The new value stored in the register Rd

    """
    Rd = (Rn << imm) | (Rn >> (32 - imm))
    return Rd


def rbit(Rd, Rn):
    """  Writes to Rd the result of reversing bits of the register Rn (unsigned).

            Parameters:
                Rd (register) : The destination ARM register
                Rn (register) : An ARM register

            Returns:
                (int) : The new value stored in the register Rd

    """
    Rd = 0
    i = 0
    while i < 32:
        Rd = (Rd << 1) + (Rn & 1)
        Rn >>= 1
        i += 1
    return Rd


#################################################################################
"""Comparison instructions"""


def cmp(Rn, n):
    """
        Sets the APSR (Application Program Status Register) N (negative), Z (zero), C (carry) and V (overflow) flags,
        based on the operation Rn-n.

            Parameters:
                Rd (register) : An ARM register
                n (register) : an immediate value or other register

    """
    m = Rn - n
    if (Rn > 0 and n < 0 and m < 0) or (Rn < 0 and n > 0 and m > 0):
        registers.V = 1
    elif not ((Rn > 0 and n < 0 and m < 0) or (Rn < 0 and n > 0 and m > 0)):
        registers.V = 0
    if m > 2147483647 or m < -2147483648:
        registers.C = 1
    elif not (m > 2147483647 or m < -2147483648):
        registers.C = 0
    if m < 0:
        registers.N = 1
    elif m > 0:
        registers.N = 0
    if m == 0:
        registers.Z = 1
    elif m != 0:
        registers.Z = 0
    return Rn


def cmn(Rn, Rm):
    """
        Sets the APSR (Application Program Status Register) N (negative), Z (zero), C (carry) and V (overflow) flags,
        based on the operation Rn+Rm.

            Parameters:
                Rn (register) : An ARM register
                Rm (register) : An ARM register

    """
    m = Rn + Rm
    if (Rn > 0 and Rm > 0 and m < 0) or (Rn < 0 and Rm < 0 and m > 0):
        registers.V = 1
    elif not ((Rn > 0 and Rm > 0 and m < 0) or (Rn < 0 and Rm < 0 and m > 0)):
        registers.V = 0
    if m > 2147483647 or m < -2147483648:
        registers.C = 1
    elif not (m > 2147483647 or m < -2147483648):
        registers.C = 0
    if m < 0:
        registers.N = 1
    elif m > 0:
        registers.N = 0
    if m == 0:
        registers.Z = 1
    elif m != 0:
        registers.Z = 0
    return Rn


def tst(Rn, Rm):
    """
        Sets the APSR (Application Program Status Register) N (negative), Z (zero), C (carry) and V (overflow) flags,
        based on the operation Rn & Rm.

            Parameters:
                Rn (register) : An ARM register
                Rm (register) : An ARM register

    """
    m = Rn & Rm
    if m < 0:
        registers.N = 1
    elif m > 0:
        registers.N = 0
    if m == 0:
        registers.Z = 1
    elif m != 0:
        registers.Z = 0
    return Rn


################################################################################
"""Branch instructions"""


def b(label, array, i):
    """
        Unconditional branch. It jumps to the ith instruction of the assembly code array.
    """
    for j in range(0, len(array)):
        j = j + 1
        if array[j] == label:
            break
    i = j
    return i


def be(label, array, i):
    """
        branch if equal. It jumps to the ith instruction of the assembly code array if Z flag is set to 1.
    """
    if registers.Z == 1:
        i = 0
        for j in range(len(array)):
            if array[j] == label:
                i = j + 1
                break
    else:
        i = i + 1
    return i


def bne(label, array, i):
    """
        branch if not equal. It jumps to the ith instruction of the assembly code array if Z flag is set to 0.
    """
    if registers.Z == 0:
        for j in range(0, len(array)):
            i = i + 1
            if array[i] == label:
                break
    else:
        i = i + 1
    return i


def bge(label, array, i):
    """
        branch if greater than or equal. It jumps to the ith instruction of the assembly code array if N flag is set
        to 0 or the Z flag is set to 1.
    """
    if registers.Z == 1 or registers.N == 0:
        for j in range(0, len(array)):
            i = i + 1
            if array[i] == label:
                break
    else:
        i = i + 1
    return i


def bgt(label, array, i):
    """
        branch if greater than. It jumps to the ith instruction of the assembly code array if N flag is set
        to 0.
    """
    if registers.N == 0:
        for j in range(0, len(array)):
            i = i + 1
            if array[i] == label:
                break
    else:
        i = i + 1
    return i


def ble(label, array, i):
    """
        branch if less than or equal. It jumps to the ith instruction of the assembly code array if N flag is set
        to 1 or the Z flag is set to 1.
    """
    if registers.Z == 1 or registers.N == 1:
        for j in range(0, len(array)):
            i = i + 1
            if array[i] == label:
                break
    else:
        i = i + 1
    return i


def blt(label, array, i):
    """
        branch if less than. It jumps to the ith instruction  of the assembly code array if N flag is set
        to 1.
    """
    if registers.N == 1:
        for j in range(0, len(array)):
            i = i + 1
            if array[i] == label:
                break
    else:
        i = i + 1
    return i

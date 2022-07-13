# This file contains the definition of some assembly functions
import ctypes

import registers
import numpy as np

"""Register move instructions"""


def MOV(Rd, n):
    """
        Writes to Rd the value of n which could be an ARM register or an 8-bit immediate value.

            Parameters:
                Rd (register) : The destination ARM register
                n (int) :  8-bit immediate value or ARM register

    """
    Rd = n
    Rd = np.int32(Rd)
    return Rd


def MOVS(Rd, n):
    """
        Writes to Rd the value of n which could be an ARM register or an 8-bit immediate value and updates N and Z flags.

            Parameters:
                Rd (register) : The destination ARM register
                n (int) :  8-bit immediate value or ARM register

    """
    Rd = n
    Rd = np.int32(Rd)
    if Rd < 0:
        registers.N = 1
        registers.Z = 0
    elif Rd > 0:
        registers.N = 0
        registers.Z = 0
    else:
        registers.Z = 1
    return Rd


def MOVW(Rd, imm16):
    """
        Writes a 16-bit immediate value to Rd.

            Parameters:
                Rd (register) : The destination ARM register
                imm16 (int) :  16-bit immediate value

    """
    Rd = imm16
    Rd = np.int32(Rd)
    return Rd


def MOVT(Rd, imm16):
    """
        Writes a 16-bit immediate value to the top half-word of a register, without affecting the bottom half-word.

            Parameters:
                Rd (register) : The destination ARM register
                imm16 (int) :  16-bit immediate value

    """
    Rd = (Rd & 0xffff) | (imm16 << 16)
    Rd = np.int32(Rd)
    return Rd


def MOVWT(Rd, imm32):
    """
        Writes a 32-bit immediate value to Rd.

            Parameters:
                Rd (register) : The destination ARM register
                imm32 (int) :  32-bit immediate value


    """
    Rd = imm32
    Rd = np.int32(Rd)
    return Rd


######################################################################################################################

"""Load register from memory"""


def LDR(Rt, Rn, imm7):
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
    Rt = np.int32(Rt)
    return Rt


def LDRB(Rt, Rn, imm5):
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
    Rt = np.int32(Rt)
    return Rt


def LDRH(Rt, Rn, imm6):
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
    Rt = np.int32(Rt)
    return Rt


######################################################################################################################

"""Store register to memory"""


def STR_(Rt, Rn, imm7):
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


def LDRB(Rt, Rn, imm5):
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


def LDRH(Rt, Rn, imm6):
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


def ADD(Rd, Rn, n , fun=None, imm=None):
    """ Writes to the register Rd the result obtained by adding the immediate value or the register n to the register Rn

            Parameters:
                Rd (register) : The destination ARM register
                Rn (register) : An ARM register
                n (int) :  immediate value or ARM register

            Returns:
                (int) : The new value stored in the register Rd

    """
    if (fun is None) and (imm is None) :
        Rd = Rn + n
        Rd = np.int32(Rd)
        return Rd
    else:
        registers.n = fun(n, n, imm)
        Rd = Rn + registers.n
        Rd = np.int32(Rd)
        return Rd




def ADDS(Rd, Rn, n):
    """ Writes to the register Rd the result obtained by adding the immediate value or the register n to the register Rn
        and updates the flags
            Parameters:
                Rd (register) : The destination ARM register
                Rn (register) : An ARM register
                n (int) :  immediate value or ARM register

            Returns:
                (int) : The new value stored in the register Rd

    """
    m = Rn + n
    if m > 2147483647 or m < -2147483648:
        registers.C = 1
    elif not (m > 2147483647 or m < -2147483648):
        registers.C = 0

    Rd = np.int32(m)
    if (Rn > 0 and n > 0 and m < 0) or (Rn < 0 and n < 0 and m > 0):
        registers.V = 1
    elif not ((Rn > 0 and n > 0 and m < 0) or (Rn < 0 and n < 0 and m > 0)):
        registers.V = 0

    if m < 0:
        registers.N = 1
        registers.Z = 0
    elif m > 0:
        registers.N = 0
        registers.Z = 0
    if m == 0:
        registers.Z = 1

    return Rd


def SUB(Rd, Rn, n , fun=None, imm=None):
    """ Writes to the register Rd the result obtained by subtracting the immediate value or the register n from
        the register Rn .

            Parameters:
                Rd (register) : The destination ARM register
                Rn (register) : An ARM register
                n (int) :  immediate value or ARM register

            Returns:
                (int) : The new value stored in the register Rd

    """
    if (fun is None) and (imm is None):
        Rd = Rn - n
        Rd = np.int32(Rd)
        return Rd
    else:
        registers.n = fun(n, n, imm)
        Rd = Rn - registers.n
        Rd = np.int32(Rd)
        return Rd


def SUBS(Rd, Rn, n):
    """ Writes to the register Rd the result obtained by subtracting the immediate value or the register n from
        the register Rn and updates the flags.

            Parameters:
                Rd (register) : The destination ARM register
                Rn (register) : An ARM register
                n (int) :  immediate value or ARM register

            Returns:
                (int) : The new value stored in the register Rd

    """
    m = Rn - n
    if m > 2147483647 or m < -2147483648:
        registers.C = 1
    elif not (m > 2147483647 or m < -2147483648):
        registers.C = 0

    Rd = np.int32(m)
    if (Rn > 0 and n < 0 and m < 0) or (Rn < 0 and n > 0 and m > 0):
        registers.V = 1
    elif not ((Rn > 0 and n < 0 and m < 0) or (Rn < 0 and n > 0 and m > 0)):
        registers.V = 0
    if m < 0:
        registers.N = 1
        registers.Z = 0
    elif m > 0:
        registers.N = 0
        registers.Z = 0
    if m == 0:
        registers.Z = 1
    return Rd


def NEG(Rd, Rn):
    """ Writes to the register Rd the negation of the register Rn

            Parameters:
                Rd (register) : The destination ARM register
                Rn (register) : An ARM register

            Returns:
                (int) : The new value stored in the register Rd

    """
    Rd = -Rn
    Rd = np.int32(Rd)
    return Rd


def MUL(Rd, Rn):
    """ Writes to the register Rd the result obtained by multiplying the register Rd by the register Rn
            Parameters:
                Rd (register) : The destination ARM register
                Rn (register) : An ARM register

            Returns:
                (int) : The new value stored in the register Rd

    """
    Rd = Rd * Rn
    Rd = np.int32(Rd)
    return Rd


def SDIV(Rd, Rn, Rm):
    """ Writes to the register Rd the result obtained after a signed division of the register Rn by the register Rm.

            Parameters:
                Rd (register) : The destination ARM register
                Rn (register) : An ARM register
                Rm (register) : An ARM register

            Returns:
                (int) : The new value stored in the register Rd

    """
    Rd = Rn / Rm
    Rd = np.int32(Rd)
    return Rd


def UDIV(Rd, Rn, Rm):
    """ Writes to the register Rd the result obtained after an unsigned division of the register Rn by the register Rm.

            Parameters:
                Rd (register) : The destination ARM register
                Rn (register) : An ARM register
                Rm (register) : An ARM register

            Returns:
                (int) : The new value stored in the register Rd

    """
    Rd = Rn / Rm
    Rd = np.int32(Rd)
    return Rd


######################################################################################################################
"""Logical instructions"""


def AND_(Rd, Rn):
    """ Writes to the register Rd the result obtained after performing a bitwise AND between Rd and Rn.

            Parameters:
                Rd (register) : The destination ARM register
                Rn (register) : An ARM register

            Returns:
                (int) : The new value stored in the register Rd

    """
    Rd &= Rn
    Rd = np.int32(Rd)
    return Rd


def ANDS(Rd, Rn):
    """ Writes to the register Rd the result obtained after performing a bitwise AND between Rd and Rn.

            Parameters:
                Rd (register) : The destination ARM register
                Rn (register) : An ARM register

            Returns:
                (int) : The new value stored in the register Rd

    """
    Rd &= Rn
    Rd = np.int32(Rd)
    if Rd < 0:
        registers.N = 1
        registers.Z = 0
    elif Rd > 0:
        registers.N = 0
        registers.Z = 0
    if Rd == 0:
        registers.Z = 1
    return Rd


def ORR(Rd, Rn):
    """ Writes to the register Rd the result obtained after performing a bitwise OR between Rd and Rn.

            Parameters:
                Rd (register) : The destination ARM register
                Rn (register) : An ARM register

            Returns:
                (int) : The new value stored in the register Rd

    """
    Rd |= Rn
    Rd = np.int32(Rd)
    return Rd


def ORRS(Rd, Rn):
    """ Writes to the register Rd the result obtained after performing a bitwise OR between Rd and Rn
        and updates the flags.

            Parameters:
                Rd (register) : The destination ARM register
                Rn (register) : An ARM register

            Returns:
                (int) : The new value stored in the register Rd

    """
    Rd |= Rn
    Rd = np.int32(Rd)
    if Rd < 0:
        registers.N = 1
        registers.Z = 0
    elif Rd > 0:
        registers.N = 0
        registers.Z = 0
    if Rd == 0:
        registers.Z = 1
    return Rd


def ERO(Rd, Rn):
    """ Writes to the register Rd the result obtained after performing a bitwise XOR between Rd and Rn.

            Parameters:
                Rd (register) : The destination ARM register
                Rn (register) : An ARM register

            Returns:
                (int) : The new value stored in the register Rd

    """
    Rd ^= Rn
    Rd = np.int32(Rd)
    return Rd


def EROS(Rd, Rn):
    """ Writes to the register Rd the result obtained after performing a bitwise XOR between Rd and Rn.

            Parameters:
                Rd (register) : The destination ARM register
                Rn (register) : An ARM register

            Returns:
                (int) : The new value stored in the register Rd

    """
    Rd ^= Rn
    Rd = np.int32(Rd)

    if Rd < 0:
        registers.N = 1
        registers.Z = 0
    elif Rd > 0:
        registers.N = 0
        registers.Z = 0
    if Rd == 0:
        registers.Z = 1
    return Rd


def MVN(Rd, Rn):
    """ Writes to the register Rd the r 1’s complement of Rn.

            Parameters:
                Rd (register) : The destination ARM register
                Rn (register) : An ARM register

            Returns:
                (int) : The new value stored in the register Rd

    """
    Rd = Rn ^ 0xffffffff
    Rd = np.int32(Rd)
    return Rd


def MVNS(Rd, Rn):
    """ Writes to the register Rd the r 1’s complement of Rn.

            Parameters:
                Rd (register) : The destination ARM register
                Rn (register) : An ARM register

            Returns:
                (int) : The new value stored in the register Rd

    """
    Rd = Rn ^ 0xffffffff
    Rd = np.int32(Rd)
    if Rd < 0:
        registers.N = 1
        registers.Z = 0
    elif Rd > 0:
        registers.N = 0
        registers.Z = 0
    if Rd == 0:
        registers.Z = 1
    return Rd


def BIC(Rd, Rn):
    """  Bit clear Rd using mask in Rn.

            Parameters:
                Rd (register) : The destination ARM register
                Rn (register) : An ARM register

            Returns:
                (int) : The new value stored in the register Rd

    """
    Rd &= ~Rn
    Rd = np.int32(Rd)
    return Rd


def BICS(Rd, Rn):
    """  Bit clear Rd using mask in Rn and updates the flags.

            Parameters:
                Rd (register) : The destination ARM register
                Rn (register) : An ARM register

            Returns:
                (int) : The new value stored in the register Rd

    """
    Rd &= ~Rn
    Rd = np.int32(Rd)
    if Rd < 0:
        registers.N = 1
        registers.Z = 0
    elif Rd > 0:
        registers.N = 0
        registers.Z = 0
    if Rd == 0:
        registers.Z = 1
    return Rd


######################################################################################################################
"""Shift and rotation instructions"""


def LSL(Rd, Rn, imm):
    """  Writes to Rd the result of left shifting Rn by imm bits.

            Parameters:
                Rd (register) : The destination ARM register
                Rn (register) : An ARM register
                imm (int) : immediate value, number of bits shifted

            Returns:
                (int) : The new value stored in the register Rd

    """
    imm = imm % 32
    Rd = Rn << imm
    Rd = np.int32(Rd)
    return Rd


def LSLS(Rd, Rn, imm):
    """  Writes to Rd the result of logical left-shifting Rn by imm bits.

            Parameters:
                Rd (register) : The destination ARM register
                Rn (register) : An ARM register
                imm (int) : immediate value, number of bits shifted

            Returns:
                (int) : The new value stored in the register Rd

    """
    imm = imm % 32
    Rd = np.int32(Rn << imm)
    if imm != 0:
        if Rd > 2147483647 or Rd < -2147483648:
            registers.C = 1
        elif not (Rd > 2147483647 or Rd < -2147483648):
            registers.C = 0
    Rd = np.int32(Rd)
    if Rd < 0:
        registers.N = 1
        registers.Z = 0
    elif Rd > 0:
        registers.N = 0
        registers.Z = 0
    if Rd == 0:
        registers.Z = 1
    return Rd


def LSR(Rd, Rn, imm):
    """  Writes to Rd the result of right shifting Rn by imm bits.

            Parameters:
                Rd (register) : The destination ARM register
                Rn (register) : An ARM register
                imm (int) : immediate value, number of bits shifted

            Returns:
                (int) : The new value stored in the register Rd

    """
    imm = imm % 32
    Rn = np.uint32(Rn)
    Rd = Rn >> imm
    Rd = np.int32(Rd)
    return Rd


def LSRS(Rd, Rn, imm):
    """  Writes to Rd the result of logical right-shifting Rn by imm bits.

            Parameters:
                Rd (register) : The destination ARM register
                Rn (register) : An ARM register
                imm (int) : immediate value, number of bits shifted

            Returns:
                (int) : The new value stored in the register Rd

    """
    imm = imm % 32
    Rd = np.uint32(Rn) >> imm
    if imm != 0:
        if Rd > 2147483647 or Rd < -2147483648:
            registers.C = 1
        elif not (Rd > 2147483647 or Rd < -2147483648):
            registers.C = 0
    Rd = np.int32(Rd)
    if Rd < 0:
        registers.N = 1
        registers.Z = 0
    elif Rd > 0:
        registers.N = 0
        registers.Z = 0
    if Rd == 0:
        registers.Z = 1
    Rd = np.int32(Rd)
    return Rd


def ASR(Rd, Rn, imm):
    """  Writes to Rd the result of arithmetic right-shifting Rn byimm bits.

            Parameters:
                Rd (register) : The destination ARM register
                Rn (register) : An ARM register
                imm (int) : immediate value, number of bits shifted

            Returns:
                (int) : The new value stored in the register Rd

    """
    Rd = Rn >> imm
    imm = imm % 32
    Rd = np.int32(Rd)
    return Rd


def ROR(Rd, Rn, imm):
    """  Writes to Rd the result of right rotating Rn by imm bits.

            Parameters:
                Rd (register) : The destination ARM register
                Rn (register) : An ARM register
                imm (int) : immediate value, number of bits rotated

            Returns:
                (int) : The new value stored in the register Rd

    """
    imm = imm % 32
    Rd = ((Rn & (2**32-1)) >> imm) | (Rn << (32-(imm)) & (2**32-1))
    Rd = np.int32(Rd)
    return Rd


def ROL(Rd, Rn, imm):
    """  Writes to Rd the result of left rotating Rn by imm bits.

            Parameters:
                Rd (register) : The destination ARM register
                Rn (register) : An ARM register
                imm (int) : immediate value, number of bits rotated

            Returns:
                (int) : The new value stored in the register Rd

    """
    imm = imm%32
    Rd = (Rn << imm) & (2**32-1) | ((Rn & (2**32-1)) >> (32-imm))
    Rd = np.int32(Rd)
    return Rd


def RBIT(Rd, Rn):
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
    Rd = np.int32(Rd)
    return Rd


#################################################################################
"""Comparison instructions"""


def CMP(Rn, n):
    """
        Sets the APSR (Application Program Status Register) N (negative), Z (zero), C (carry) and V (overflow) flags,
        based on the operation Rn-n.

            Parameters:
                Rd (register) : An ARM register
                n (register) : an immediate value or other register

    """
    m = Rn - n
    if m > 2147483647 or m < -2147483648:
        registers.C = 1
    elif not (m > 2147483647 or m < -2147483648):
        registers.C = 0
    m = np.int32(m)
    if (Rn > 0 and n < 0 and m < 0) or (Rn < 0 and n > 0 and m > 0):
        registers.V = 1
    elif not ((Rn > 0 and n < 0 and m < 0) or (Rn < 0 and n > 0 and m > 0)):
        registers.V = 0
    if m < 0:
        registers.N = 1
        registers.Z = 0
    elif m > 0:
        registers.N = 0
        registers.Z = 0
    if m == 0:
        registers.Z = 1
    return Rn


def CMN(Rn, Rm):
    """
        Sets the APSR (Application Program Status Register) N (negative), Z (zero), C (carry) and V (overflow) flags,
        based on the operation Rn+Rm.

            Parameters:
                Rn (register) : An ARM register
                Rm (register) : An ARM register

    """
    m = Rn + Rm
    if m > 2147483647 or m < -2147483648:
        registers.C = 1
    elif not (m > 2147483647 or m < -2147483648):
        registers.C = 0
    m = np.int32(m)
    if (Rn > 0 and Rm > 0 and m < 0) or (Rn < 0 and Rm < 0 and m > 0):
        registers.V = 1
    elif not ((Rn > 0 and Rm > 0 and m < 0) or (Rn < 0 and Rm < 0 and m > 0)):
        registers.V = 0
    if m < 0:
        registers.N = 1
    elif m > 0:
        registers.N = 0
    if m == 0:
        registers.Z = 1
    elif m != 0:
        registers.Z = 0
    return Rn


def TST(Rn, Rm):
    """
        Sets the APSR (Application Program Status Register) N (negative), Z (zero), C (carry) and V (overflow) flags,
        based on the operation Rn & Rm.

            Parameters:
                Rn (register) : An ARM register
                Rm (register) : An ARM register

    """
    Rd = Rn & Rm
    if Rd < 0:
        registers.N = 1
        registers.Z = 0
    elif Rd > 0:
        registers.N = 0
        registers.N = 0
        registers.Z = 0
    if Rd == 0:
        registers.Z = 1
    return Rn


################################################################################
"""Branch instructions"""


def B(label, array, i):
    """
        Unconditional branch. It jumps to the ith instruction of the assembly code array.
    """
    i = 0
    for j in range(len(array)):
        if array[j] == label:
            i = j + 1
            break
    return i


def BE(label, array, i):
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


def BNE(label, array, i):
    """
        branch if not equal. It jumps to the ith instruction of the assembly code array if Z flag is set to 0.
    """
    if registers.Z == 0:
        i = 0
        for j in range(len(array)):
            if array[j] == label:
                i = j + 1
                break
    else:
        i = i + 1
    return i


def BGE(label, array, i):
    """
        branch if greater than or equal. It jumps to the ith instruction of the assembly code array if N flag is set
        to 0 or the Z flag is set to 1.
    """
    if registers.Z == 1 or registers.N == 0:
        i = 0
        for j in range(len(array)):
            if array[j] == label:
                i = j + 1
                break
    else:
        i = i + 1
    return i


def BGT(label, array, i):
    """
        branch if greater than. It jumps to the ith instruction of the assembly code array if N flag is set
        to 0.
    """
    if registers.N == 0:
        i = 0
        for j in range(len(array)):
            if array[j] == label:
                i = j + 1
                break
    else:
        i = i + 1
    return i


def BLE(label, array, i):
    """
        branch if less than or equal. It jumps to the ith instruction of the assembly code array if N flag is set
        to 1 or the Z flag is set to 1.
    """
    if registers.Z == 1 or registers.N == 1:
        i = 0
        for j in range(len(array)):
            if array[j] == label:
                i = j + 1
                break
    else:
        i = i + 1
    return i


def BLT(label, array, i):
    """
        branch if less than. It jumps to the ith instruction  of the assembly code array if N flag is set
        to 1.
    """
    if registers.N == 1:
        i = 0
        for j in range(len(array)):
            if array[j] == label:
                i = j + 1
                break
    else:
        i = i + 1
    return i

################################################################################


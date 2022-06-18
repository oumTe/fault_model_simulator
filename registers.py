"""

This file includes the global variables that, in our situation, represent the registers.
By default, they are set to zero.

"""
import numpy as np

def initialize():
    global R0
    global R1
    global R2
    global R3
    global R4
    global R5
    global R6
    global R7
    global R8
    global R9
    global R10
    global R11
    global R12
    global R13
    global R14
    global R15
    global Z
    global N
    global C
    global V
    global memory

    """Registers"""
    R0 = np.int32(0)
    R1 = np.int32(0)
    R2 = np.int32(0)
    R3 = np.int32(0)
    R4 = np.int32(0)
    R5 = np.int32(0)
    R6 = np.int32(0)
    R7 = np.int32(0)
    R8 = np.int32(0)
    R9 = np.int32(0)
    R10 = np.int32(0)
    R11 = np.int32(0)
    R12 = np.int32(0)
    R13 = np.int32(110)
    R14 = np.int32(180)
    R15 = np.int32(250)

    """Flags"""
    Z = 0
    N = 0
    C = 0
    V = 0

    """Memory array"""
    memory = [0] * 4000

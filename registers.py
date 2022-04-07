"""

This file includes the global variables that, in our situation, represent the registers.
By default, they are set to zero.

"""


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
    global Z
    global N
    global C
    global V
    global memory

    """Registers"""
    R0 = 0
    R1 = 0
    R2 = 0
    R3 = 0
    R4 = 0
    R5 = 0
    R6 = 0
    R7 = 0
    R8 = 0
    R9 = 0
    R10 = 0
    R11 = 0
    R12 = 0

    """Flags"""
    Z = 0
    N = 0
    C = 0
    V = 0

    """Memory array"""
    memory = [0] * 4000

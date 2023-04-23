
from .math_util import derp

def darken(c, amount):

    return normalize(c[0]-amount, c[1]-amount, c[2]-amount)

def normalize(*c):
    def clip(cp):
        return max(0,min(cp,255))
    return tuple(clip(int(cp)) for cp in c)

def mult_color(c, mult):
    return normalize(c[0]*mult, c[1]*mult, c[2]*mult)

def mix(A, B, p):

    return normalize(*(derp(ac, bc, p) for ac, bc in zip(A,B)))

def magic(A,B,xp):

    try:
        return (xp,B[0] + ((B[1]-B[0])/(A[1]-A[0])) * (xp - A[0]))
    except ZeroDivisionError:
        return A
    
def lerp(x1: float, x2: float, y1: float, y2: float, x: float):
    """Perform linear interpolation for x between (x1,y1) and (x2,y2) """

    return ((y2 - y1) * x + x2 * y1 - x1 * y2) / (x2 - x1)

def derp(n1, n2, p):

    return lerp(0,1,n1,n2,p)
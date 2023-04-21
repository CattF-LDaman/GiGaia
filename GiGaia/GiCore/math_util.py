
def magic(A,B,xp):

    try:
        return (xp,B[0] + ((B[1]-B[0])/(A[1]-A[0])) * (xp - A[0]))
    except ZeroDivisionError:
        return A

def darken(c, amount):

    return normalize(c[0]-amount, c[1]-amount, c[2]-amount)

def normalize(*c):
    def clip(cp):
        return max(0,min(cp,255))
    return tuple(clip(int(cp)) for cp in c)
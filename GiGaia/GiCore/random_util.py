import random

def seeded_randchoice(seed,c):
    random.seed(seed)
    return random.choice(c)

def seeded_randint(seed,x1,x2):
    random.seed(seed)
    return random.randint(x1,x2)
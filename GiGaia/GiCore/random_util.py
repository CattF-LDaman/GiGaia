import random

def seeded_randchoice(c, seed):
    random.seed(seed)
    return random.choice(c)

def seeded_randint(x1, x2, seed):
    random.seed(seed)
    return random.randint(x1,x2)
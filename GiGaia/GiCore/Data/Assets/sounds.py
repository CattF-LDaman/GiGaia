
import os
import pygame

def load(man):

    man.instance.log("[ASSETS] Loading sounds...")
    sdir = os.path.join(man.location,"Sounds")
    for sfile in os.listdir(sdir):
        sname, ext = os.path.splitext(sfile)
        if ext != ".ogg":
            man.instance.log(f"[ASSETS] Non ogg file '{sfile}' in sounds! Ignoring.",3)
            continue
        s = pygame.mixer.Sound(os.path.join(sdir,sfile))
        man.assets["sounds"][sname] = s
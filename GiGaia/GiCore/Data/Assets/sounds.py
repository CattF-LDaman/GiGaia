
import os
import pygame

def load(man):

    if type(man.instance).__name__ == "Server":
        return

    man.instance.log("[ASSETS] Loading sounds...")
    sdir = os.path.join(man.location,"Sounds")
    for sfile in os.listdir(sdir):
        sname, ext = os.path.splitext(sfile)
        if ext not in [".ogg",".wav"]:
            man.instance.log(f"[ASSETS] Unsupported sound file extension '{sfile}' in sounds! Ignoring.",3)
            continue
        s = pygame.mixer.Sound(os.path.join(sdir,sfile))
        man.assets["sounds"][sname] = s
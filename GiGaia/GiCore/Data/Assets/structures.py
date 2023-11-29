
from GiGaia.GiCore.Game.World.structuredata import StructureData

from types import SimpleNamespace
import pygame
import os

def load(man):
    man.instance.log("[ASSETS] Loading structures...")

    man.structures = {}

    sdir = os.path.join(man.location,"Structures")
    for sfile in os.listdir(sdir):
        sname, ext = os.path.splitext(sfile)
        if ext != ".gigs":
            man.instance.log(f"[ASSETS] Unsupported structure file extension '{sfile}' in structures! Ignoring.",3)
            continue
        man.structures[sname] = StructureData(os.path.join(sdir, sfile))
    
    man.STRUCTURES = SimpleNamespace(**{k.upper():v for k,v in man.structures.items()})
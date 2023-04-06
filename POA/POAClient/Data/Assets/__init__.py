
from . import font

import traceback
import os
import pygame
import pathlib
import json
import types

class AssetsManager:

    def __init__(self, client):

        self.client = client
        self.location = client.dirs["assets"]

        self.assets = {"fonts":{}, "icon":None, "data":{}, "sounds":{}}

    def __getitem__(self, indx):
        return self.assets.get(indx)

    def load(self):

        self.client.log("[ASSETS] Loading datafiles...")
        datadir = os.path.join(self.location,"Data")
        for root, dirs, files in os.walk(datadir):
            for name in files:
                dataname, ext = os.path.splitext(name)
                if ext != ".json":
                    self.client.log("[ASSETS] Non json file in datafiles! Ignoring.",3)
                    continue
                datapath = os.path.join(root, name)
                try:
                    with open(datapath,"r") as f:
                        datacont = json.load(f)
                except json.decoder.JSONDecodeError as e:
                    self.client.log(f"[ASSETS] Bad datafile '{datapath}': \n{''.join(traceback.format_exception(e, value=e ,tb=e.__traceback__))}",4)
                    continue
                pathpart = pathlib.Path(datapath).relative_to(datadir).parts[0]
                if pathpart and not self.assets["data"].get(pathpart):
                    self.assets["data"][pathpart] = {}
                if pathpart and pathpart!=name:
                    if dataname in self.assets["data"][pathpart]:
                        self.client.log(f"[ASSETS] Name collision in datafiles: {pathpart}/{dataname}",3)
                    self.assets["data"][pathpart][dataname] = datacont
                else:
                    if dataname in self.assets["data"]:
                        self.client.log(f"[ASSETS] Name collision in datafiles: {dataname}",3)
                    self.assets["data"][dataname] = datacont   
        nd = {}
        for k, v in self.assets["data"].items():
            if isinstance(v, dict):
                v = types.SimpleNamespace(**v)
            nd[k] = v
        self.assets["data"] = types.SimpleNamespace(**nd)

        self.client.log("[ASSETS] Loading fonts...")
        for fontfile in os.listdir(os.path.join(self.location, "Fonts")):
            fpath = os.path.join(self.location, "Fonts")
            fontname, ext = os.path.splitext(fontfile)
            if ext == ".png":
                self.assets["fonts"][fontname] = font.Font(fpath, fontname)

        self.client.log("[ASSETS] Loading sounds...")
        sdir = os.path.join(self.location,"Sounds")
        for sfile in os.listdir(sdir):
            sname, ext = os.path.splitext(sfile)
            if ext != ".ogg":
                self.client.log(f"[ASSETS] Non ogg file '{sfile}' in sounds! Ignoring.",3)
                continue
            s = pygame.mixer.Sound(os.path.join(sdir,sfile))
            self.assets["sounds"][sname] = s

        self.client.log("[ASSETS] Loading icon...")
        self.assets['icon'] = pygame.transform.scale(pygame.image.load(os.path.join(self.location,'icon.png')),(64,64))

        self.assets = types.SimpleNamespace(**self.assets)
        self.client.log("[ASSETS] Done loading assets.")

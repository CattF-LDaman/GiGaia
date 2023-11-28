
import types
import json
import traceback
import pathlib
import os

def load(man):

    man.instance.log("[ASSETS] Loading datafiles...")
    datadir = os.path.join(man.location,"Data")
    for root, dirs, files in os.walk(datadir):
        for name in files:
            dataname, ext = os.path.splitext(name)
            if ext != ".json":
                man.instance.log(f"[ASSETS] Non json file '{name}' in datafiles! Ignoring.",3)
                continue
            datapath = os.path.join(root, name)
            try:
                with open(datapath,"r") as f:
                    datacont = json.load(f)
            except json.decoder.JSONDecodeError as e:
                man.instance.log(f"[ASSETS] Bad datafile '{datapath}': \n{''.join(traceback.format_exception(e, value=e ,tb=e.__traceback__))}",4)
                continue
            pathpart = pathlib.Path(datapath).relative_to(datadir).parts[0]
            if pathpart and not man.assets["data"].get(pathpart):
                man.assets["data"][pathpart] = {}
            if pathpart and pathpart!=name:
                if dataname in man.assets["data"][pathpart]:
                    man.instance.log(f"[ASSETS] Name collision in datafiles: {pathpart}/{dataname}",3)
                man.assets["data"][pathpart][dataname] = datacont
            else:
                if dataname in man.assets["data"]:
                    man.instance.log(f"[ASSETS] Name collision in datafiles: {dataname}",3)
                man.assets["data"][dataname] = datacont   
    nd = {}
    for k, v in man.assets["data"].items():
        if isinstance(v, dict):
            v = types.SimpleNamespace(**v)
        nd[k] = v
    man.assets["data"] = types.SimpleNamespace(**nd)

from .assetpack import ASSETS, PASS

import tempfile
import py7zr
import os

def extract_assets(loc, build):

    with tempfile.TemporaryDirectory(prefix="GiGaia") as tempdir:
        temp = os.path.join(tempdir, "GiGAsset")
        with open(temp,"wb") as tempf:
            tempf.write(ASSETS)
        with py7zr.SevenZipFile(temp, "r", password=PASS) as archive:
            archive.extractall(path=loc)

    with open(os.path.join(loc, "build"), "w") as bf:
        bf.write(build)

def check_assets(loc, build):

    assets_loc = os.path.join(loc, "assets")
    if os.path.exists(os.path.join(assets_loc, "build")):
        with open(os.path.join(assets_loc,"build"), "r") as f:
            build_f = f.read()
            return build_f == build
    return False

import py7zr
import os

APY = "ASSETS = {}\nPASS='{}'\n"

def create_assetpack(dir, assetsdir):

    ap_pass = os.urandom(7).hex()
    assetpack = os.path.join(dir, "assets")
    with py7zr.SevenZipFile(assetpack, "w", password=ap_pass) as af:
        af.writeall(assetsdir, ".")

    with open(os.path.join(dir,"Installer","assetpack.py"), "w") as f:
        with open(assetpack, "rb") as apf:
            f.write(APY.format(str(apf.read()), ap_pass))
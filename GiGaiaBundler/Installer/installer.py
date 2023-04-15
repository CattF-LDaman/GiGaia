
import os

from .assets import check_assets, extract_assets

def run(loc, build):

    if not check_assets(loc, build):
        extract_assets(os.path.join(loc,"assets"), build)


import os
import time
import sys

from getpass import getuser

def add_build(dir):

    build_id = f'{sys.platform}-{getuser().encode("utf-8").hex()[:3]}-{int(time.time())}'

    with open(os.path.join(dir, "GiGaia", "GiCore", "version.py"), "a") as vf:

        vf.write(f"\nBUILD = '{build_id}'\n")

    return build_id
import os
import datetime
import time
import sys

from getpass import getuser

def add_build(dir):

    build_id = f'{sys.platform}-{getuser().encode("utf-8").hex()[:3]}-{int(time.time()*100)}-{datetime.datetime.now().strftime("%d%m%y")}'

    with open(os.path.join(dir, "GiGaia", "GiCore", "version.py"), "a") as vf:

        vf.write(f"\nBUILD = '{build_id}'\n")

    return build_id
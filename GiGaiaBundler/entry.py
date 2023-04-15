
import os

ENTRY_CONTENT = """
import sys
from os import environ
environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

from GiGaia.Gi{trg}.{trgLower} import {trg}
from GiGaia.GiCore.version import BUILD
from GiGaia.GiCore.Data import get_data_dir

from Installer import installer

bundle_type = '{trg}'
if bundle_type == "Server":
    loc = sys.argv[1] if len (sys.argv) > 1 else "./GiGaiaServer"
else:
    loc = get_data_dir("GiGaia")

if __name__ == "__main__":
    installer.run(loc, BUILD)
    {trg}(loc).run()
"""

def create(dir, target):

    with open(os.path.join(dir, f"run_{target.lower()}.py"), "w") as rf:

        rf.write(ENTRY_CONTENT.format(trgLower=target.lower(), trg=target))

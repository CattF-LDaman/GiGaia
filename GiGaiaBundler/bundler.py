import os
import shutil

from . import entry
from . import assets
from . import version

def bundle(bundle_target):

    print(f"Bundling {bundle_target}...")

    bundle_dir = "./bundler_temp"

    print(f"Copying source to {bundle_dir}...")
    shutil.copytree("GiGaia",os.path.join(bundle_dir,"GiGaia"), dirs_exist_ok=True)
    print("Done.")

    print("Adding installer...")
    shutil.copytree("GiGaiaBundler/Installer", os.path.join(bundle_dir,"Installer"))
    print("Done.")

    print("Creating assetpack...")
    assets.create_assetpack(bundle_dir, "GiGaia_Assets")
    print("Done.")

    print("Creating entry point...")
    entry.create(bundle_dir, bundle_target)
    print("Done.")

    print("Adding build information to source...")
    build = version.add_build(bundle_dir)
    print(f"Build: {build}")
    print("Done.")

    os.chdir(bundle_dir)

    print(f"Running Pyinstaller in {bundle_dir}...")

    os.system(f'pyinstaller run_{bundle_target.lower()}.py --distpath "../bundled" --workpath bundler_wp -i "../GiGaia_Assets/icon.ico" --onefile -n "GiGaia{bundle_target}"'+(' --noconsole' if bundle_target == 'Client' else ''))
    print("Done.")

    os.chdir("..")

    print("Removing temporary files...")
    shutil.rmtree(bundle_dir)
    print("Done.")

    print(f"Finished bundling GiGaia{bundle_target} ({build}).")

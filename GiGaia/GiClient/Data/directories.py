import os

def create_directory_structure(client_dir):

    dirnames = ["logs","configs","assets","screenshots","structures"]
    dirs = {dn:os.path.join(client_dir, dn) for dn in dirnames}

    for d in dirs.values():
        os.makedirs(d, exist_ok=True)

    return dirs
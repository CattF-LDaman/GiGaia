from .bundler import bundle

print("Bundle target?")
print("[0] Client")
print("[1] Server")
print("[2] Both")

while True:
    try:
        bundle_target = ["Client","Server", "Both"][int(input("> "))]
        break
    except IndexError:
        print("! Choice should be 0 or 1 !")
        continue

if bundle_target == "Both":
    bundle("Client")
    bundle("Server")
else:
    bundle(bundle_target)


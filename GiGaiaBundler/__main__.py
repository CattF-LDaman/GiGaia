from .bundler import bundle

print("Bundle target?")
print("[0] Client")
print("[1] Server")
print("[2] Both")
print("(3) Custom build ID")

custom_build_id = None
while True:
    try:
        inp = int(input("> "))
        if inp == 3:
            custom_build_id = input("BUILD ID: ")
            continue
        bundle_target = ["Client","Server", "Both"][inp]
        break
    except (IndexError, ValueError):
        print("! Invalid choice !")
        continue

if bundle_target == "Both":
    bundle("Client", custom_build_id)
    bundle("Server", custom_build_id)
else:
    bundle(bundle_target, custom_build_id)



import os

def generate_key():

    initial_bytes = bytearray(b for b in range(256))
    key = bytearray()

    for _ in range(256):

        key.append(initial_bytes.pop(os.urandom(1)[0]%len(initial_bytes)))

    return key

class SessionObfuscator:  # Makes it harder but still very trivial to read/change network traffic

    def __init__(self, in_key, out_key):

        self.in_key = in_key
        self.out_key = out_key

    def obf(self,data:bytes):

        return data.translate(bytes.maketrans(bytearray(b for b in range(256)),self.out_key))

    def deobf(self,data:bytes):

        return data.translate(bytes.maketrans(self.in_key,bytearray(b for b in range(256))))

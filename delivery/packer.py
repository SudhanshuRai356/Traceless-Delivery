import struct
from crypto.encrypt import hybrid_encrypt

def pack_payload(public_key_path: str, infile: str, outfile: str):
    data = open(infile, "rb").read()
    pkg = hybrid_encrypt(public_key_path, data)
    enc_key = pkg["encrypted_aes_key"]
    iv = pkg["iv"]
    tag = pkg["tag"]
    cipher = pkg["ciphertext"]
    blob = struct.pack(">I", len(enc_key)) + enc_key + iv + tag + cipher
    open(outfile, "wb").write(blob)

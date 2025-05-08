import struct
from crypto.rsa import loadkeypair, decrypt as rsa_decrypt
from crypto.aes import decrypt as aes_decrypt

def load_payload(payload_path: str, private_key_path: str) -> bytes:
    data = open(payload_path, "rb").read()
    enc_key_len = struct.unpack(">I", data[:4])[0]
    offset = 4
    enc_key = data[offset:offset+enc_key_len]; offset += enc_key_len
    iv = data[offset:offset+12]; offset += 12
    tag = data[offset:offset+16]; offset += 16
    ciphertext = data[offset:]
    private = loadkeypair(private_key_path)
    aes_key = rsa_decrypt(private, enc_key)
    plaintext = aes_decrypt(aes_key, iv, ciphertext, tag)
    return plaintext

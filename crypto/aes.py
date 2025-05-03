from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os
def genkey(key_size=32):
    key = os.urandom(key_size)
    return key
def encrypt(key, plaintext) -> tuple[bytes, bytes, bytes]:
    iv = os.urandom(12) # since we are going to be using GCM mode, we need a 12 byte IV
    encryptor = Cipher(algorithms.AES(key), modes.GCM(iv), backend=default_backend()).encryptor()
    cipher=encryptor.update(plaintext) + encryptor.finalize()
    return iv,cipher,encryptor.tag
def decrypt(key, iv, ciphertext, tag) -> bytes:
    decryptor = Cipher(algorithms.AES(key), modes.GCM(iv, tag), backend=default_backend()).decryptor()
    plaintext = decryptor.update(ciphertext) + decryptor.finalize()
    return plaintext
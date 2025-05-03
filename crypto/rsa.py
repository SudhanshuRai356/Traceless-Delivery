from cryptography.hazmat.primitives.asymmetric import rsa,padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend
def genkey(key_size=2048):
    private=rsa.generate_private_key(
        public_exponent=65537,
        key_size=key_size,
        backend=default_backend()
    )
    public=private.public_key()
    return private,public
def savekeypair(private,filepath='privatekey.pem'):
    pem=private.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,  #basic format for private keys and PKCS8 is a standard for private key storage
        encryption_algorithm=serialization.NoEncryption()
    )
    with open(filepath,'wb') as f:
        f.write(pem)
def savepublickey(public,filepath='publickey.pem'):
    pem=public.public_bytes(
        encoding=serialization.Encoding.PEM,   #standard encoding for public keys
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    with open(filepath,'wb') as f:
        f.write(pem)
def loadkeypair(filepath='privatekey.pem'):
    with open(filepath,'rb') as f:
        data=f.read()
    private=serialization.load_pem_private_key(
        data,
        password=None,  #since we did NoEncryption in the encryption_algorithm when saving the private key
        backend=default_backend()
    )
    return private
def loadpublickey(filepath='publickey.pem'):
    with open(filepath,'rb') as f:
        data=f.read()
    public=serialization.load_pem_public_key(
        data,
        backend=default_backend()
    )
    return public
def encrypt(public,plaintext):
    ciphertext=public.encrypt(
        plaintext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),  #mask generation function from the OAEP standard 
            algorithm=hashes.SHA256(),  #hash function used in OAEP
            label=None
        )
    )
    return ciphertext
def decrypt(private,ciphertext):
    plaintext=private.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),  #mask generation function from the OAEP standard 
            algorithm=hashes.SHA256(),  #hash function used in OAEP
            label=None
        )
    )
    return plaintext

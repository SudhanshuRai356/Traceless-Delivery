from crypto.rsa import loadpublickey, loadkeypair,encrypt as rsa_encrypt, decrypt as rsa_decrypt
from crypto.aes import genkey as generate_aes_key, encrypt as aes_encrypt, decrypt as aes_decrypt
def hybrid_encrypt(public_key_path,plaintext):
    pubkey=loadpublickey(public_key_path)
    aes_key=generate_aes_key()
    encrypted_aes_key=rsa_encrypt(pubkey,aes_key)
    iv,ciphertext,tag=aes_encrypt(aes_key,plaintext)
    return{
        'encrypted_aes_key':encrypted_aes_key,
        'iv':iv,
        'ciphertext':ciphertext,
        'tag':tag
    }
def hybrid_decrypt(keypair_path,package):
    private_key=loadkeypair(keypair_path)
    aes_key=rsa_decrypt(private_key,package['encrypted_aes_key'])
    plaintext=aes_decrypt(aes_key,package['iv'],package['ciphertext'],package['tag'])
    return plaintext
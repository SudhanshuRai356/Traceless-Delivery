# Run this script to generate a new RSA key pair and save them to files, you can change file names as required and please do not
# share the private key file but you will need to share the public key so that other user can send messages to you while keeping them encrypted
# and private 
from crypto.rsa import genkey, savekeypair, savepublickey
def main():
    private, public = genkey()
    savekeypair(private, 'privatekey.pem')
    savepublickey(public, 'publickey.pem')
    print("Keys generated and saved as 'privatekey.pem' and 'publickey.pem'")
if __name__ == "__main__":
    main()
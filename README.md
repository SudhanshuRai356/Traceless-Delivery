# Traceless-Delivery
A encrypted payload delivery system 
This program is a delivery system which uses a hybrid encryption to encrypt and send payloads which can be only by the person it was meant for as it uses an Asymmetric system using RSA for one part of the hybrid encryption
## File Path
```
Traceless-Delivery
├──main.py
├──generatekeys.py
├──payloads/
│ ├──__init__.py
│ ├──sample.py
├──delivery/
│ ├──__init__.py
│ ├──loader.py
│ ├──packer.py
├──crypto/
│ ├──__init__.py
│ ├──aes.py
│ ├──encrypt.py
│ ├──rsa.py
```
## Working
The system works by first using the generate keys function to generate a key pair for rsa which is unique to the person, we generate the keys using the RSA module of the pycryptodome's cryptography module.
The Public key is to be shared while the private key should be kept well private
The main.py when ran needs to be given the command line arguement of laod,pack or terminal
For pack the other command line arguments need to be the public key file, input file path and output path in that order
### Packing
In packing the file's data is encrypted with an AES GCM mode process using randomised key, tag and IV and then the key, tag and IV are encoded using the RSA public key and appended to the AES encrypted data and outputted to the specified path
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
For load the other command line arguments need to be the input encrypted file path, private key path and the output file path in that order
### Loading
In the loading process the file's initial bytes are taken and decoded using the Private key of the RSA to get the Key, tag and IV and then the key, tag and IV are used to decoded the rest of the file encrypted with AES
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
The terminal arguement is a cli option menu which guides through the process
## Steps to Run
1. Clone the repo into your system and go to the Traceless-Delivery Folder
```
git clone https://github.com/SudhanshuRai-Flme/Traceless-Delivery.git
cd Traceless-Delivery
```
2.  Install the required python modules or just run the below command in your opened terminal
    ```
    pip install -r requirements.txt
    ```
3. In the terminal openned in the Traceless-Delivery folder run the the main file in the required mode
```
python main.py <mode> <arg 1> <arg 2> <arg 3>
```
arguement are not required for terminal mode but required for the other modes
4. Before Encoding the package with pack the public key of whoever the package needs to be sent to needs to be on the users system
5. While decoding a package meant for the user(i.e, the package was encoded using the user's public key) the users private key needs to be used
## Features
Uses hybrid encryption (RSA + AES) for secure payload delivery
All decryption happens in memory
Supports any file type: .py, .txt, .json, binaries, etc.
Includes both interactive mode and command-line interface
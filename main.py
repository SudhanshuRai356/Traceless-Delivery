import sys
from delivery.packer import pack_payload
from delivery.loader import load_payload

def main():
    if sys.argv[1] == "terminal":
        print("Choose whether to pack or load the payload")
        choice = input("Enter 'pack' to pack the payload or 'load' to load the payload: ")
        if choice == "pack":
            public_key_path = input("Enter the path to the public key file: ")
            infile = input("Enter the path to the input file: ")
            outfile = input("Enter the path to the output binary file: ")
            pack_payload(public_key_path, infile, outfile)
            print(f"The encrypted payload is saved as {outfile}")
        elif choice == "load":
            payload_path = input("Enter the path to the payload binary file: ")
            private_key_path = input("Enter the path to the private key file: ")
            outfile = input("Enter the path to the output file: ")
            data = load_payload(payload_path, private_key_path)
            with open(outfile, "wb") as f:
                f.write(data)
            print(f"The decrypted payload is saved as {outfile}")
        else:
            print("Unknown command. Use 'pack' or 'load'. Please rerun the script.")
            return
    elif len(sys.argv) != 5:
        print("Guide:")
        print("To run the script in interactive mode run the script with the format main.py terminal")
        print("To pack the data you need to run the script with the format main.py pack <public_key.pem> <input_file> <output_bin>")
        print("To load the data from the encrypted file you need to run the script with the format main.py load <payload_bin> <keypair.pem> <output_file>")
        return
    command = sys.argv[1]
    if command == "pack":
        public_key_path = sys.argv[2]
        infile = sys.argv[3]
        outfile = sys.argv[4]
        pack_payload(public_key_path, infile, outfile)
        print(f"The encrypted payload is saved as {outfile}")
    elif command == "load":
        payload_path = sys.argv[2]
        private_key_path = sys.argv[3]
        outfile = sys.argv[4]
        data = load_payload(payload_path, private_key_path)
        with open(outfile, "wb") as f:
            f.write(data)
        print(f"The decrypted payload is saved as {outfile}")
    else:
        print("Unknown command. Please rerun the script and use 'pack' or 'load' or 'terminal'.")

if __name__ == "__main__":
    main()

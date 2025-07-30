import tkinter as tk
from tkinter import filedialog, messagebox
import ctypes
from delivery.packer import pack_payload
from delivery.loader import load_payload
from crypto.rsa import genkey, savekeypair, savepublickey

class TracelessGUI:
    def __init__(self, root):
        self.root = root
        
        # Make it crisp on Windows
        try:
            ctypes.windll.shcore.SetProcessDpiAwareness(1)
        except:
            pass
        
        self.root.title("Traceless Delivery")
        self.root.geometry("500x450")
        self.root.configure(bg='#1e1e1e')
        self.root.resizable(False, False)
        
        # Force proper scaling
        self.root.tk.call('tk', 'scaling', 1.33)
        
        self.setup_ui()
        
    def setup_ui(self):
        # Title
        title = tk.Label(self.root, text="TRACELESS DELIVERY", font=('Segoe UI', 16, 'bold'), bg='#1e1e1e', fg='#00ff41')
        title.pack(pady=10)
        
        # Main container
        main = tk.Frame(self.root, bg='#1e1e1e')
        main.pack(fill=tk.BOTH, expand=True, padx=20, pady=5)
        
        # Generate Keys Section
        keys_frame = tk.LabelFrame(main, text="GENERATE KEYS", font=('Segoe UI', 9, 'bold'),bg='#1e1e1e', fg='#ffffff', bd=1, relief='solid')
        keys_frame.pack(fill=tk.X, pady=5)
        
        keys_inner = tk.Frame(keys_frame, bg='#1e1e1e')
        keys_inner.pack(padx=10, pady=6)
        
        # Key name input
        name_frame = tk.Frame(keys_inner, bg='#1e1e1e')
        name_frame.pack(fill=tk.X, pady=4)
        tk.Label(name_frame, text="Key Name:", font=('Segoe UI', 8), bg='#1e1e1e', fg='#ffffff').pack(side=tk.LEFT)
        self.key_name = tk.Entry(name_frame, font=('Segoe UI', 8), width=20, bg='#404040', fg='#ffffff', insertbackground='#ffffff', relief='flat')
        self.key_name.pack(side=tk.LEFT, padx=8)
        self.key_name.insert(0, "mykey")
        
        tk.Button(keys_inner, text="GENERATE RSA KEYS", command=self.gen_keys,font=('Segoe UI', 9, 'bold'), bg='#0d7377', fg='#ffffff',width=18, height=2, relief='flat', cursor='hand2').pack(pady=4)
        
        # Encrypt Section
        enc_frame = tk.LabelFrame(main, text="ENCRYPT FILE", font=('Segoe UI', 9, 'bold'),bg='#1e1e1e', fg='#ffffff', bd=1, relief='solid')
        enc_frame.pack(fill=tk.X, pady=5)
        
        enc_inner = tk.Frame(enc_frame, bg='#1e1e1e')
        enc_inner.pack(padx=10, pady=6)
        
        enc_row1 = tk.Frame(enc_inner, bg='#1e1e1e')
        enc_row1.pack(fill=tk.X, pady=2)
        tk.Button(enc_row1, text="Public Key", command=lambda: self.pick_file('enc_pub'),font=('Segoe UI', 8), bg='#404040', fg='#ffffff', width=11, relief='flat', cursor='hand2').pack(side=tk.LEFT)
        self.enc_pub_label = tk.Label(enc_row1, text="No file selected", font=('Segoe UI', 8), bg='#1e1e1e', fg='#888888')
        self.enc_pub_label.pack(side=tk.LEFT, padx=8)
        
        enc_row2 = tk.Frame(enc_inner, bg='#1e1e1e')
        enc_row2.pack(fill=tk.X, pady=2)
        tk.Button(enc_row2, text="Input File", command=lambda: self.pick_file('enc_in'),font=('Segoe UI', 8), bg='#404040', fg='#ffffff', width=11, relief='flat', cursor='hand2').pack(side=tk.LEFT)
        self.enc_in_label = tk.Label(enc_row2, text="No file selected", font=('Segoe UI', 8), bg='#1e1e1e', fg='#888888')
        self.enc_in_label.pack(side=tk.LEFT, padx=8)
        
        tk.Button(enc_inner, text="ENCRYPT", command=self.encrypt_file,font=('Segoe UI', 9, 'bold'), bg='#ff6b35', fg='#ffffff',width=13, height=1, relief='flat', cursor='hand2').pack(pady=6)
        
        # Decrypt Section
        dec_frame = tk.LabelFrame(main, text="DECRYPT FILE", font=('Segoe UI', 9, 'bold'),bg='#1e1e1e', fg='#ffffff', bd=1, relief='solid')
        dec_frame.pack(fill=tk.X, pady=5)
        
        dec_inner = tk.Frame(dec_frame, bg='#1e1e1e')
        dec_inner.pack(padx=10, pady=6)
        
        dec_row1 = tk.Frame(dec_inner, bg='#1e1e1e')
        dec_row1.pack(fill=tk.X, pady=2)
        tk.Button(dec_row1, text="Encrypted File", command=lambda: self.pick_file('dec_in'),font=('Segoe UI', 8), bg='#404040', fg='#ffffff', width=11, relief='flat', cursor='hand2').pack(side=tk.LEFT)
        self.dec_in_label = tk.Label(dec_row1, text="No file selected", font=('Segoe UI', 8), bg='#1e1e1e', fg='#888888')
        self.dec_in_label.pack(side=tk.LEFT, padx=8)
        
        dec_row2 = tk.Frame(dec_inner, bg='#1e1e1e')
        dec_row2.pack(fill=tk.X, pady=2)
        tk.Button(dec_row2, text="Private Key", command=lambda: self.pick_file('dec_key'),font=('Segoe UI', 8), bg='#404040', fg='#ffffff', width=11, relief='flat', cursor='hand2').pack(side=tk.LEFT)
        self.dec_key_label = tk.Label(dec_row2, text="No file selected", font=('Segoe UI', 8), bg='#1e1e1e', fg='#888888')
        self.dec_key_label.pack(side=tk.LEFT, padx=8)
        
        tk.Button(dec_inner, text="DECRYPT", command=self.decrypt_file,font=('Segoe UI', 9, 'bold'), bg='#004e89', fg='#ffffff', width=13, height=1, relief='flat', cursor='hand2').pack(pady=6)
        
        # Initialize file paths
        self.files = {
            'enc_pub': '', 'enc_in': '', 'dec_in': '', 'dec_key': ''
        }
        
    def pick_file(self, file_type):
        if file_type in ['enc_pub', 'dec_key']:
            file = filedialog.askopenfilename(filetypes=[("PEM files", "*.pem")])
        elif file_type == 'dec_in':
            file = filedialog.askopenfilename(filetypes=[("BIN files", "*.bin")])
        else:
            file = filedialog.askopenfilename()
            
        if file:
            self.files[file_type] = file
            filename = file.replace('\\', '/').split('/')[-1]
            
            if file_type == 'enc_pub':
                self.enc_pub_label.config(text=filename, fg='#00ff41')
            elif file_type == 'enc_in':
                self.enc_in_label.config(text=filename, fg='#00ff41')
            elif file_type == 'dec_in':
                self.dec_in_label.config(text=filename, fg='#00ff41')
            elif file_type == 'dec_key':
                self.dec_key_label.config(text=filename, fg='#00ff41')
                
    def gen_keys(self):
        key_name = self.key_name.get().strip()
        if not key_name:
            key_name = "mykey"
        
        private_file = f"{key_name}_private.pem"
        public_file = f"{key_name}_public.pem"
        
        private, public = genkey()
        savekeypair(private, private_file)
        savepublickey(public, public_file)
        messagebox.showinfo("Done", f"Keys saved as:\n{private_file}\n{public_file}")
        
    def encrypt_file(self):
        if not self.files['enc_pub'] or not self.files['enc_in']:
            messagebox.showerror("Error", "Select both files first")
            return
            
        output = filedialog.asksaveasfilename(defaultextension=".bin", filetypes=[("BIN files", "*.bin")])
        if not output:
            return
            
        pack_payload(self.files['enc_pub'], self.files['enc_in'], output)
        messagebox.showinfo("Done", f"Encrypted and saved as:\n{output.replace('\\', '/').split('/')[-1]}")
        
    def decrypt_file(self):
        if not self.files['dec_in'] or not self.files['dec_key']:
            messagebox.showerror("Error", "Select both files first")
            return
            
        output = filedialog.asksaveasfilename()
        if not output:
            return
            
        data = load_payload(self.files['dec_in'], self.files['dec_key'])
        with open(output, "wb") as f:
            f.write(data)
        messagebox.showinfo("Done", f"Decrypted and saved as:\n{output.replace('\\', '/').split('/')[-1]}")

def main():
    root = tk.Tk()
    app = TracelessGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()

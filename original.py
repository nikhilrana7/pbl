import os
import threading
from tkinter import Tk, filedialog, Button, Label, messagebox

class Action:
    ENCRYPT = "encrypt"
    DECRYPT = "decrypt"

class ProcessManager:
    def __init__(self, file_path, action):
        self.file_path = file_path
        self.action = action

    def read_env_key(self):
        env_file = ".env"
        if not os.path.exists(env_file):
            with open(env_file, 'w') as f:
                f.write("4")  # default key

        with open(env_file, 'r') as f:
            return int(f.read().strip())

    def run(self):
        try:
            key = self.read_env_key()

            # Read content in binary mode
            with open(self.file_path, 'rb') as f:
                content = f.read()

            modified = bytearray()
            for byte in content:
                if self.action == Action.ENCRYPT:
                    modified.append((byte + key) % 256)
                else:
                    modified.append((byte - key + 256) % 256)

            # Write back modified content
            with open(self.file_path, 'wb') as f:
                f.write(modified)
                f.flush()
                os.fsync(f.fileno())

            messagebox.showinfo("Success", f"{self.action.capitalize()}ion successful!")

            # Ask to view the file
            if messagebox.askyesno("Open File", "Do you want to open the file to check?"):
                os.startfile(self.file_path)

        except Exception as e:
            messagebox.showerror("Error", f"Error: {str(e)}")

class EncryptorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Encryptor / Decryptor")
        self.root.geometry("400x200")
        self.file_path = ""

        self.label = Label(root, text="Step 1: Select a file")
        self.label.pack(pady=10)

        self.select_button = Button(root, text="Choose File", command=self.select_file)
        self.select_button.pack()

        self.encrypt_button = Button(root, text="Encrypt", state="disabled", command=self.encrypt_file)
        self.encrypt_button.pack(pady=5)

        self.decrypt_button = Button(root, text="Decrypt", state="disabled", command=self.decrypt_file)
        self.decrypt_button.pack(pady=5)

    def select_file(self):
        path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if path:
            self.file_path = path
            self.label.config(text=f"Selected: {os.path.basename(path)}")
            self.encrypt_button.config(state="normal")
            self.decrypt_button.config(state="normal")

    def encrypt_file(self):
        self.process(Action.ENCRYPT)

    def decrypt_file(self):
        self.process(Action.DECRYPT)

    def process(self, action):
        if not self.file_path:
            messagebox.showerror("Error", "No file selected")
            return
        thread = threading.Thread(target=ProcessManager(self.file_path, action).run)
        thread.start()

if __name__ == "__main__":
    root = Tk()
    app = EncryptorApp(root)
    root.mainloop()
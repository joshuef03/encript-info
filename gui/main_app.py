import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext

from core.crypto_utils import encriptar_texto, desencriptar_texto
from core.file_handler import encriptar_archivo, desencriptar_archivo
from core.validators import validar_contraseña, manejar_error


class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Encriptador SHA-256 + Fernet")
        self.root.geometry("600x500")

        # Entrada de contraseña
        tk.Label(root, text="Contraseña:").pack()
        self.entry_password = tk.Entry(root, show="*")
        self.entry_password.pack(fill=tk.X, padx=10)

        # Área de texto
        tk.Label(root, text="Texto:").pack()
        self.text_area = scrolledtext.ScrolledText(root, height=10)
        self.text_area.pack(fill=tk.BOTH, expand=True, padx=10)

        # Botones de texto
        tk.Button(root, text="Encriptar Texto", command=self.encriptar_texto_gui).pack(pady=2)
        tk.Button(root, text="Desencriptar Texto", command=self.desencriptar_texto_gui).pack(pady=2)

        # Separador visual
        tk.Label(root, text="").pack()

        # Botones de archivo
        tk.Button(root, text="Encriptar Archivo", command=self.encriptar_archivo_gui).pack(pady=2)
        tk.Button(root, text="Desencriptar Archivo", command=self.desencriptar_archivo_gui).pack(pady=2)

    def get_password(self):
        pwd = self.entry_password.get()
        validar_contraseña(pwd)
        return pwd

    def encriptar_texto_gui(self):
        try:
            texto = self.text_area.get("1.0", tk.END).strip()
            password = self.get_password()
            resultado = encriptar_texto(texto, password)
            self.text_area.delete("1.0", tk.END)
            self.text_area.insert(tk.END, resultado)
        except Exception as e:
            messagebox.showerror("Error", manejar_error(e))

    def desencriptar_texto_gui(self):
        try:
            texto = self.text_area.get("1.0", tk.END).strip()
            password = self.get_password()
            resultado = desencriptar_texto(texto, password)
            self.text_area.delete("1.0", tk.END)
            self.text_area.insert(tk.END, resultado)
        except Exception as e:
            messagebox.showerror("Error", manejar_error(e))

    def encriptar_archivo_gui(self):
        path = filedialog.askopenfilename()
        if not path:
            return
        try:
            password = self.get_password()
            salida = encriptar_archivo(path, password)
            messagebox.showinfo("Éxito", f"Archivo encriptado:\n{salida}")
        except Exception as e:
            messagebox.showerror("Error", manejar_error(e))

    def desencriptar_archivo_gui(self):
        path = filedialog.askopenfilename(filetypes=[("Archivos Encriptados", "*.enc")])
        if not path:
            return
        try:
            password = self.get_password()
            salida = desencriptar_archivo(path, password)
            messagebox.showinfo("Éxito", f"Archivo desencriptado:\n{salida}")
        except Exception as e:
            messagebox.showerror("Error", manejar_error(e))


def iniciar_app():
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()
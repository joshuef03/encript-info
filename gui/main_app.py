import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from pathlib import Path

from core.db_connector import insertar_archivo
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
        
        # Separador visual
        tk.Label(root, text="").pack()

        # Botones de Base de datos
        tk.Button(root, text="Guardar en BD", command=self.guardar_en_bd_gui).pack(pady=2)
        tk.Button(root, text="Explorar BD y Desencriptar", command=self.explorar_db_gui).pack(pady=2)

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

    def guardar_en_bd_gui(self):
        path = filedialog.askopenfilename(filetypes=[("Archivos Encriptados", "*.enc")])
        if not path:
            return
        try:
            file_path = Path(path)
            with file_path.open("rb") as f:
                binary_data = f.read()
            insertar_archivo(file_path.name, binary_data)
            messagebox.showinfo("Éxito", "Archivo guardado en la base de datos.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def explorar_db_gui(self):
        from pathlib import Path
        import tkinter.simpledialog as simpledialog
        from core.db_connector import obtener_archivos, descargar_archivo
        from core.file_handler import RAW_DIR
        from core.crypto_utils import desencriptar_bytes

        try:
            archivos = obtener_archivos()
            if not archivos:
                messagebox.showinfo("BD Vacía", "No hay archivos almacenados.")
                return

            opciones = "\n".join([f"{id}: {name}" for id, name in archivos])
            seleccion = simpledialog.askinteger("Explorador BD", f"ID del archivo a recuperar:\n\n{opciones}")
            if seleccion is None:
                return

            nombre, data_encriptada = descargar_archivo(seleccion)
            password = self.get_password()

            # Desencriptar bytes
            try:
                datos = desencriptar_bytes(data_encriptada, password)
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo desencriptar: {e}")
                return

            # Guardar en RAW_DIR
            nombre_original = nombre
            if nombre.endswith(".enc"):
                nombre_original = Path(nombre).with_suffix("").name
            ruta_salida = RAW_DIR / nombre_original

            contador = 1
            while ruta_salida.exists():
                nombre_base = Path(nombre_original).stem
                extension = Path(nombre_original).suffix
                ruta_salida = RAW_DIR / f"{nombre_base}_v{contador}{extension}"
                contador += 1

            with ruta_salida.open("wb") as f:
                f.write(datos)

            messagebox.showinfo("Éxito", f"Archivo recuperado y desencriptado:\n{ruta_salida}")
        except Exception as e:
            messagebox.showerror("Error", f"Error al explorar BD:\n{e}")

def iniciar_app():
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()
#F3NIX
import subprocess
import speedtest
import requests
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import webbrowser

# Función para procesar un archivo
def procesar_archivo(archivo):
    palabras = set()
    with open(archivo, 'r', encoding='utf-8', errors='ignore') as file:
        for line in file:
            palabras.update(line.split())
    return palabras

# Función para agregar archivos
def agregar_archivo():
    archivo = filedialog.askopenfilename(filetypes=[("Archivos de texto", "*.txt")])
    if archivo:
        archivos_seleccionados.append(archivo)
        archivos_seleccionados_label.config(text="Archivos seleccionados:\n" + "\n".join(archivos_seleccionados))

# Función para generar el resultado
def generar_resultado():
    palabras_unicas = set()
    for archivo in archivos_seleccionados:
        palabras_unicas.update(procesar_archivo(archivo))
    
    resultado = 'resultado.txt'
    with open(resultado, 'w') as file:
        file.write('\n'.join(palabras_unicas))

    resultado_label.config(text=f'Se han creado {len(palabras_unicas)} palabras únicas en {resultado}')

# Función para realizar un escaneo ARP
def escanear_arp():
    try:
        # Obtener la contraseña del Entry
        contrasena = contrasena_entry.get()
        comando = f'sudo -S arp-scan --localnet'
        resultado_arp = subprocess.check_output(comando, shell=True, input=f'{contrasena}\n'.encode()).decode('utf-8')
        resultado_label.config(text=f'Resultado ARP Scan:\n{resultado_arp}')
    except subprocess.CalledProcessError as e:
        resultado_label.config(text=f'Error al ejecutar arp-scan: {e}')

# Función para medir la velocidad de internet
def medir_velocidad():
    st = speedtest.Speedtest()
    descarga = st.download() / 1024 / 1024
    subida = st.upload() / 1024 / 1024
    ping = st.results.ping
    resultado_label.config(text=f'Velocidad de Descarga: {descarga:.2f} Mbps\nVelocidad de Subida: {subida:.2f} Mbps\nPing: {ping} ms')

# Función para obtener la dirección IP y abrir Google Maps
def obtener_ip_y_abrir_mapa():
    try:
        ip = requests.get('https://ipinfo.io').text
        resultado_label.config(text=f'Dirección IP: {ip}')
        
        if ip:
            ip_info = requests.get(f'https://ipinfo.io/{ip}/json').json()
            if 'loc' in ip_info:
                lat, lon = ip_info['loc'].split(',')
                maps_url = f'https://www.google.com/maps/place/{lat},{lon}'
                subprocess.Popen(['xdg-open', maps_url])
    except requests.RequestException:
        resultado_label.config(text='Error al obtener la dirección IP.')

# Función para borrar metadatos de un archivo
def borrar_metadatos(archivo):
    try:
        subprocess.run(["exiftool", "-all=", archivo])
        resultado_label.config(text=f'Se han borrado los metadatos de {archivo}')
    except FileNotFoundError:
        resultado_label.config(text='ExifTool no está instalado. Por favor, instálelo para utilizar esta función.')

# Función para elegir archivo para borrar metadatos
def elegir_archivo_borrar_metadatos():
    archivo = filedialog.askopenfilename(filetypes=[("Todos los archivos", "*.*")])
    if archivo:
        borrar_metadatos_button.config(state="normal")
        archivos_seleccionados.append(archivo)
        archivos_seleccionados_label.config(text="Archivo seleccionado para borrar metadatos:\n" + archivo)

# Función para cifrar una carpeta
def encrypt_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        subprocess.run(["tar", "czf", "-", folder_path], stdout=subprocess.PIPE)
        subprocess.run(["gpg", "-c", "-o", folder_path + ".tar.gz.gpg"], stdin=subprocess.PIPE)

# Función para descifrar una carpeta
def decrypt_folder():
    file_path = filedialog.askopenfilename()
    if file_path:
        gpg_process = subprocess.Popen(["gpg", "-d", "-o", file_path[:-7]], stdin=subprocess.PIPE)
        with open(file_path, "rb") as encrypted_file:
            gpg_process.communicate(encrypted_file.read())

# Función para extraer metadatos EXIF de una imagen
def get_exif_data(image):
    exif_data = {}
    info = image._getexif()
    if info:
        for tag, value in info.items():
            decoded = TAGS.get(tag, tag)
            exif_data[decoded] = value
    return exif_data

# Función para extraer información GPS de los metadatos EXIF
def get_gps_info(exif_data):
    gps_info = {}
    if "GPSInfo" in exif_data:
        for key in exif_data["GPSInfo"].keys():
            decode = GPSTAGS.get(key, key)
            gps_info[decode] = exif_data["GPSInfo"][key]
    return gps_info

# Función para convertir grados, minutos y segundos a formato decimal
def get_decimal_from_dms(dms, ref):
    degrees = float(dms[0])
    minutes = float(dms[1])
    seconds = float(dms[2])

    decimal = degrees + (minutes / 60.0) + (seconds / 3600.0)
    if ref in ['S', 'W']:
        decimal = -decimal
    return decimal

# Función para obtener las coordenadas de latitud y longitud
def get_coordinates(gps_info):
    lat = None
    lon = None

    if 'GPSLatitude' in gps_info and 'GPSLatitudeRef' in gps_info and 'GPSLongitude' in gps_info and 'GPSLongitudeRef' in gps_info:
        lat = get_decimal_from_dms(gps_info['GPSLatitude'], gps_info['GPSLatitudeRef'])
        lon = get_decimal_from_dms(gps_info['GPSLongitude'], gps_info['GPSLongitudeRef'])

    return lat, lon

# Función para abrir Google Maps con las coordenadas especificadas
def open_google_maps(lat, lon):
    url = f"https://www.google.com/maps/place/{lat},{lon}"
    webbrowser.open(url)

# Función para buscar un archivo de imagen y extraer su ubicación GPS
def buscar_archivo_y_abrir_mapa():
    archivo = filedialog.askopenfilename(filetypes=[("Todos los archivos", "*.*")])
    if archivo:
        try:
            image = Image.open(archivo)
            exif_data = get_exif_data(image)
            gps_info = get_gps_info(exif_data)
            lat, lon = get_coordinates(gps_info)
            if lat and lon:
                open_google_maps(lat, lon)
            else:
                messagebox.showinfo("GPS Info", "No GPS información encontrada en la imagen.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo procesar el archivo de imagen.\nError: {e}")

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Programa Combinado F3NIX")

# Lista para almacenar los archivos seleccionados
archivos_seleccionados = []

# Botones
style = ttk.Style()
style.configure('Boton3D.TButton', relief='raised', borderwidth=5, background='black', foreground='green')

# Botón para agregar archivo
agregar_button = ttk.Button(ventana, text="Agregar Archivo", command=agregar_archivo, style='Boton3D.TButton')
agregar_button.grid(row=0, column=0, padx=5, pady=5)

# Botón para generar resultado
generar_button = ttk.Button(ventana, text="Generar Resultado", command=generar_resultado, style='Boton3D.TButton')
generar_button.grid(row=1, column=0, padx=5, pady=5)

# Entry para contraseña de sudo
contrasena_entry = tk.Entry(ventana, show="*", bg='black', fg='green')
contrasena_entry.grid(row=2, column=0, padx=5, pady=5)

# Botón para escanear ARP
escanear_arp_button = ttk.Button(ventana, text="Escanear ARP", command=escanear_arp, style='Boton3D.TButton')
escanear_arp_button.grid(row=3, column=0, padx=5, pady=5)

# Botón para medir velocidad de internet
velocidad_button = ttk.Button(ventana, text="Medir Velocidad de Internet", command=medir_velocidad, style='Boton3D.TButton')
velocidad_button.grid(row=4, column=0, padx=5, pady=5)

# Botón para obtener IP y abrir mapa
mapa_button = ttk.Button(ventana, text="Obtener IP y Abrir Mapa", command=obtener_ip_y_abrir_mapa, style='Boton3D.TButton')
mapa_button.grid(row=5, column=0, padx=5, pady=5)

# Botón para elegir archivo para borrar metadatos
elegir_archivo_borrar_metadatos_button = ttk.Button(ventana, text="Elegir Archivo para Borrar Metadatos", command=elegir_archivo_borrar_metadatos, style='Boton3D.TButton')
elegir_archivo_borrar_metadatos_button.grid(row=6, column=0, padx=5, pady=5)

# Botón para borrar metadatos
borrar_metadatos_button = ttk.Button(ventana, text="Borrar Metadatos", command=lambda: borrar_metadatos(archivos_seleccionados[0]), style='Boton3D.TButton', state="disabled")
borrar_metadatos_button.grid(row=7, column=0, padx=5, pady=5)

# Botón para cifrar carpeta
encrypt_folder_button = ttk.Button(ventana, text="Cifrar Carpeta", command=encrypt_folder, style='Boton3D.TButton')
encrypt_folder_button.grid(row=0, column=1, padx=5, pady=5)

# Botón para descifrar carpeta
decrypt_button = ttk.Button(ventana, text="Descifrar Carpeta", command=decrypt_folder, style='Boton3D.TButton')
decrypt_button.grid(row=1, column=1, padx=5, pady=5)

# Botón para buscar archivo y abrir mapa con ubicación GPS
gps_button = ttk.Button(ventana, text="Buscar Imagen y Abrir Mapa", command=buscar_archivo_y_abrir_mapa, style='Boton3D.TButton')
gps_button.grid(row=2, column=1, padx=5, pady=5)

# Etiqueta para mostrar archivos seleccionados
archivos_seleccionados_label = tk.Label(ventana, text="Archivos seleccionados:", bg='black', fg='green')
archivos_seleccionados_label.grid(row=8, column=0, columnspan=2, padx=5, pady=5)

# Etiqueta para mostrar el resultado
resultado_label = tk.Label(ventana, text="", bg='black', fg='green')
resultado_label.grid(row=9, column=0, columnspan=2, padx=5, pady=5)

ventana.configure(bg='black')  # Cambia el color de fondo de la ventana principal
ventana.mainloop()

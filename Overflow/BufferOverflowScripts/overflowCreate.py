import argparse

def generate_pattern(buffer_length, offset_length=0, rest_length=0):
    """
    Genera una cadena en la que:
    - Los caracteres del buffer se rellenan con 'A'.
    - El segmento del offset se llena con 'B'.
    - El resto se llena con 'C'.
    
    Args:
        buffer_length (int): Longitud del segmento del buffer (relleno con 'A').
        offset_length (int): Longitud del segmento del offset (relleno con 'B').
        rest_length (int): Longitud del segmento del resto (relleno con 'C').
        
    Returns:
        str: Cadena generada.
    """
    buffer_segment = 'A' * buffer_length
    offset_segment = 'B' * offset_length
    rest_segment = 'C' * rest_length
    return buffer_segment + offset_segment + rest_segment

def main():
    parser = argparse.ArgumentParser(description="Generador de patrones para buffer overflow.")
    parser.add_argument('-b', '--buffer', type=int, required=True, help="Tamaño del segmento para desbordar el buffer (relleno con 'A').")
    parser.add_argument('-o', '--offset', type=int, default=0, help="Tamaño del segmento del offset (relleno con 'B').")
    parser.add_argument('-p', '--padding', type=int, default=0, help="Tamaño del segmento restante (relleno con 'C').")
    
    args = parser.parse_args()
    
    # Validar que `-o` y `-p` dependen de `-b`
    if args.offset and not args.buffer:
        print("Error: El argumento '-o' depende de '-b'. Usa '-b' para especificar el buffer primero.")
        return
    if args.padding and not (args.buffer and args.offset):
        print("Error: El argumento '-p' depende de '-b' y '-o'. Usa ambos antes de '-p'.")
        return
    
    # Generar patrón
    pattern = generate_pattern(args.buffer, args.offset, args.padding)
    print("\n=== Patrón Generado ===")
    print(pattern)

if __name__ == "__main__":
    main()

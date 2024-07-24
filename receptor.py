import math

# Función para calcular el número de bits de paridad necesarios
def calculate_parity_bits(m):
    for r in range(m):
        if (m + r + 1) <= 2**r:
            return r
    return 0  # En caso de error, aunque no debería ocurrir

# Función para verificar que el input sea binario
def is_binary(str):
    return all(c in '01' for c in str)

# Función para detectar y corregir errores en un mensaje codificado usando el código de Hamming
def hamming_decode(encoded_data):
    n = len(encoded_data)
    r = int(math.log2(n + 1))
    m = n - r

    error_position = 0

    # Calcular las posiciones de los bits de paridad y comprobar errores
    for i in range(r):
        parity_pos = 2**i
        parity = 0
        for j in range(1, n + 1):
            if j & parity_pos:
                parity ^= int(encoded_data[j - 1])
        error_position += parity * parity_pos

    if error_position:
        print(f"Error detected at position: {error_position}")
        encoded_data = list(encoded_data)
        encoded_data[error_position - 1] = '0' if encoded_data[error_position - 1] == '1' else '1'
        encoded_data = ''.join(encoded_data)
        print(f"Corrected encoded message: {encoded_data}")

    # Extraer los bits de datos
    decoded_data = []
    for i in range(1, n + 1):
        if (i & (i - 1)) != 0:
            decoded_data.append(encoded_data[i - 1])

    return ''.join(decoded_data)

def main():
    encoded_message = input("Enter the encoded binary message: ")

    if not is_binary(encoded_message):
        print("Error: The message must be binary (contain only 0s and 1s).")
        return

    decoded_message = hamming_decode(encoded_message)
    print(f"Decoded message: {decoded_message}")

if __name__ == "__main__":
    main()

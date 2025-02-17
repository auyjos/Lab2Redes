import socket
import math
import matplotlib.pyplot as plt
import numpy as np

# Función para calcular el número de bits de paridad necesarios
def calculate_parity_bits(m):
    for r in range(m):
        if (m + r + 1) <= 2**r:
            return r
    return 0

# Función para verificar que el input sea binario
def is_binary(s):
    return all(c in '01' for c in s)

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
        encoded_data = list(encoded_data)
        encoded_data[error_position - 1] = '0' if encoded_data[error_position - 1] == '1' else '1'
        encoded_data = ''.join(encoded_data)

    # Extraer los bits de datos
    decoded_data = []
    for i in range(1, n + 1):
        if (i & (i - 1)) != 0:
            decoded_data.append(encoded_data[i - 1])

    return ''.join(decoded_data), error_position

# Función para calcular el checksum de Fletcher
def fletcher_checksum(data, block_size=16):
    if block_size not in [8, 16, 32]:
        raise ValueError("Block size must be 8, 16, or 32")

    if len(data) % block_size != 0:
        padding_size = block_size - (len(data) % block_size)
        data += '0' * padding_size

    sum1 = 0
    sum2 = 0

    for i in range(0, len(data), block_size):
        block = data[i:i + block_size]
        block_value = int(block, 2)
        sum1 = (sum1 + block_value) % 255
        sum2 = (sum2 + sum1) % 255

    return (sum2 << 8) | sum1

# Función para decodificar mensaje en ASCII
def decode_ascii(binary_message):
    decoded = ""
    for i in range(0, len(binary_message), 8):
        byte = binary_message[i:i + 8]
        decoded += chr(int(byte, 2))
    return decoded

# Función principal del receptor
def main():
    host = '127.0.0.1'
    port = 12345

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print("Server listening...")

    received_messages = 0
    corrected_messages = 0
    error_messages = 0
    error_positions = []
    all_errors = []
    checksum_errors = []

    while True:
        conn, addr = server_socket.accept()
        print(f"Connected by {addr}")

        while True:
            data = conn.recv(1024)
            if not data:
                break

            received_message = data.decode('utf-8')
            if not is_binary(received_message):
                print("Error: The received message must be binary (contain only 0s and 1s).")
                conn.send(b'Error')
                continue

            # Calcular el checksum antes de cualquier corrección
            original_checksum = fletcher_checksum(received_message)

            # Decodificar el mensaje con Hamming
            decoded_message, error_position = hamming_decode(received_message)
            
            # Calcular el checksum después de la corrección
            corrected_checksum = fletcher_checksum(decoded_message)

            # Comparar checksums
            if original_checksum != corrected_checksum:
                print(f"Checksum error detected: {original_checksum} != {corrected_checksum}")
                checksum_errors.append(1)
            else:
                checksum_errors.append(0)

            if error_position:
                print(f"Error detected and corrected at position: {error_position}")
                error_messages += 1
                all_errors.append(1)
                error_positions.append(error_position)
            else:
                print("No errors detected.")
                corrected_messages += 1
                all_errors.append(0)
                conn.send(b'Correct')

            print(f"Received: {received_message}")
            print(f"Decoded: {decode_ascii(decoded_message)}")

            received_messages += 1
            print(f"Total messages received: {received_messages}")
            print(f"Corrected messages: {corrected_messages}")
            print(f"Error messages: {error_messages}")

        conn.close()
        print("Connection closed.")

        if received_messages >= 100:  # Ajusta esto según sea necesario
            break


if __name__ == '__main__':
    main()

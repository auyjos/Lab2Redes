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
def decodeASCII(binaryMessage):
    decoded = ""
    for i in range(0, len(binaryMessage), 8):
        byte = binaryMessage[i:i + 8]
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

            received_checksum = fletcher_checksum(received_message)
            decoded_message, error_position = hamming_decode(received_message)
            recalculated_checksum = fletcher_checksum(decoded_message)
            
            if received_checksum != recalculated_checksum:
                print("Checksum verification failed! Possible error detected.")
                error_messages += 1
                all_errors.append(1)
                error_positions.append(error_position)
                conn.send(b'Error')
            else:
                print("Checksum verification passed. Message is intact.")
                corrected_messages += 1
                all_errors.append(0)
                conn.send(b'Correct')

            received_messages += 1
            original_message = decodeASCII(decoded_message)
            print(f"Original message: {original_message}")

        conn.close()
        print("Connection closed.")
        
        # Mostrar estadísticas
        print(f"Total messages received: {received_messages}")
        print(f"Messages corrected: {corrected_messages}")
        print(f"Messages with errors: {error_messages}")

        # Graficar estadísticas
        labels = ['Corrected', 'Errors']
        sizes = [corrected_messages, error_messages]
        colors = ['lightgreen', 'lightcoral']
        explode = (0.1, 0)  # Explode the corrected messages

        plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)
        plt.axis('equal')
        plt.title('Message Correction Statistics')
        plt.savefig('message_correction_statistics.png')  # Exportar gráfico
        plt.close()

        # Graficar distribución de errores
        plt.hist(all_errors, bins=[0, 1, 2], edgecolor='black')
        plt.xticks([0, 1], ['Correct', 'Error'])
        plt.xlabel('Message Status')
        plt.ylabel('Frequency')
        plt.title('Distribution of Errors')
        plt.savefig('error_distribution.png')  # Exportar gráfico
        plt.close()

        # Graficar posiciones de error
        if error_positions:
            plt.hist(error_positions, bins=range(1, len(received_message) + 2), edgecolor='black')
            plt.xlabel('Position of Error')
            plt.ylabel('Frequency')
            plt.title('Error Positions in Messages')
            plt.savefig('error_positions.png')  # Exportar gráfico
            plt.close()

if __name__ == "__main__":
    main()

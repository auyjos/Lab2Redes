import socket
import math

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

    decoded_data = []
    for i in range(1, n + 1):
        if (i & (i - 1)) != 0:
            decoded_data.append(encoded_data[i - 1])

    return ''.join(decoded_data)

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

# Función para decodificar el mensaje en ASCII binario
def decodeASCII(binaryMessage):
    decoded = ""
    for i in range(0, len(binaryMessage), 8):
        byte = binaryMessage[i:i+8]
        decoded += chr(int(byte, 2))
    return decoded

def main():
    host = 'localhost'
    port = 12345

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print('Server listening...')
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            data = conn.recv(1024).decode()
            if not data:
                return

            print(f"Received encoded message: {data}")

            if not is_binary(data):
                print("Error: The received message must be binary (contain only 0s and 1s).")
                return

            received_checksum = fletcher_checksum(data)
            print(f"Calculated Fletcher checksum: {received_checksum}")

            decoded_message = hamming_decode(data)
            print(f"Decoded message: {decoded_message}")

            recalculated_checksum = fletcher_checksum(decoded_message)
            if received_checksum == recalculated_checksum:
                print("Checksum verification failed! Possible error detected.")
            else:
                print("Checksum verification passed. Message is intact.")

            original_message = decodeASCII(decoded_message)
            print(f"Original message: {original_message}")

if __name__ == "__main__":
    main()

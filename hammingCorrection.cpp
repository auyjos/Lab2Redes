#include <iostream>
#include <vector>
#include <cstdlib>
#include <ctime>
#include <cstring>
#include <sys/socket.h>
#include <netinet/in.h>
#include <unistd.h>
#include <arpa/inet.h> // Necesario para inet_pton

// Función para calcular el número de bits de paridad necesarios
int calculateParityBits(int m) {
    for (int r = 0; r < m; r++) {
        if ((m + r + 1) <= (1 << r)) {
            return r;
        }
    }
    return 0; // En caso de error, aunque no debería ocurrir
}

// Función para codificar un mensaje usando el código de Hamming
std::string hammingEncode(const std::string &data) {
    int m = data.size();
    int r = calculateParityBits(m);
    int n = m + r;

    std::vector<char> encodedData(n, '0');

    int j = 0;
    for (int i = 1; i <= n; i++) {
        if ((i & (i - 1)) == 0) {
            encodedData[i - 1] = 'P';
        } else {
            encodedData[i - 1] = data[j];
            j++;
        }
    }

    for (int i = 0; i < r; i++) {
        int parityPos = 1 << i;
        int parity = 0;
        for (int j = 1; j <= n; j++) {
            if (j & parityPos) {
                parity ^= (encodedData[j - 1] == '1') ? 1 : 0;
            }
        }
        encodedData[parityPos - 1] = (parity == 0) ? '0' : '1';
    }

    return std::string(encodedData.begin(), encodedData.end());
}

// Función para aplicar ruido a un mensaje con una probabilidad específica
std::string applyNoise(const std::string &message, double errorRate) {
    std::string noisyMessage = message;
    for (size_t i = 0; i < noisyMessage.size(); ++i) {
        if ((rand() / (RAND_MAX + 1.0)) < errorRate) {
            noisyMessage[i] = (noisyMessage[i] == '0') ? '1' : '0';
        }
    }
    return noisyMessage;
}

// Función para generar un mensaje binario aleatorio de longitud aleatoria
std::string generateRandomBinaryMessage(int minLength, int maxLength) {
    int length = rand() % (maxLength - minLength + 1) + minLength;
    std::string message;
    for (int i = 0; i < length; i++) {
        message += (rand() % 2) ? '1' : '0';
    }
    return message;
}

// Función para enviar un mensaje usando sockets
void sendMessage(const std::string &message) {
    int sock = socket(AF_INET, SOCK_STREAM, 0);
    if (sock < 0) {
        std::cerr << "Error creating socket" << std::endl;
        return;
    }

    sockaddr_in serverAddr;
    serverAddr.sin_family = AF_INET;
    serverAddr.sin_port = htons(12345);

    // Convertir IP de texto a formato binario
    if (inet_pton(AF_INET, "127.0.0.1", &serverAddr.sin_addr) <= 0) {
        std::cerr << "Invalid address" << std::endl;
        close(sock);
        return;
    }

    if (connect(sock, (sockaddr *)&serverAddr, sizeof(serverAddr)) < 0) {
        std::cerr << "Connection failed" << std::endl;
        close(sock);
        return;
    }

    send(sock, message.c_str(), message.size(), 0);
    close(sock);
}

int main() {
    srand(static_cast<unsigned int>(time(0))); // Semilla para la generación de números aleatorios

    int numMessages = 100; // Número de mensajes a enviar
    double errorRate = 1.0 / 100; // Tasa de error de 1/1000
    int minLength = 8; // Longitud mínima de los mensajes
    int maxLength = 64; // Longitud máxima de los mensajes

    for (int i = 0; i < numMessages; i++) {
        std::string binaryMessage = generateRandomBinaryMessage(minLength, maxLength);
        std::cout << "Binary message: " << binaryMessage << std::endl;

        std::string encodedMessage = hammingEncode(binaryMessage);
        std::string noisyMessage = applyNoise(encodedMessage, errorRate);

        sendMessage(noisyMessage);
    }

    return 0;
}

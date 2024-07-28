#include <iostream>
#include <vector>
#include <cmath>
#include <string>
#include <bitset>
#include <cstdlib>
#include <ctime>
#include <cstring>
#include <arpa/inet.h>
#include <unistd.h>

#define PORT 12345
#define ERROR_PROBABILITY 0.001

// Funciones de la capa de presentación
std::string charToBinary(char c) {
    return std::bitset<8>(c).to_string();
}

std::string encodeASCII(const std::string &message) {
    std::string encoded;
    for (char c : message) {
        encoded += charToBinary(c);
    }
    return encoded;
}

std::string decodeASCII(const std::string &binaryMessage) {
    std::string decoded;
    for (size_t i = 0; i < binaryMessage.size(); i += 8) {
        std::bitset<8> byte(binaryMessage.substr(i, 8));
        decoded += char(byte.to_ulong());
    }
    return decoded;
}

// Funciones de la capa de enlace
int calculateParityBits(int m) {
    for (int r = 0; r < m; r++) {
        if ((m + r + 1) <= std::pow(2, r)) {
            return r;
        }
    }
    return 0;
}

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
        int parityPos = std::pow(2, i);
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

// Funciones de la capa de ruido
std::string applyNoise(const std::string &data, double errorRate) {
    std::string noisyData = data;
    for (char &c : noisyData) {
        if ((rand() / (double)RAND_MAX) < errorRate) {
            c = (c == '0') ? '1' : '0';
        }
    }
    return noisyData;
}

// Funciones de la capa de transmisión
void sendMessage(const std::string &message) {
    int sock = 0;
    struct sockaddr_in serv_addr;

    if ((sock = socket(AF_INET, SOCK_STREAM, 0)) < 0) {
        std::cerr << "Socket creation error" << std::endl;
        return;
    }

    serv_addr.sin_family = AF_INET;
    serv_addr.sin_port = htons(PORT);

    if (inet_pton(AF_INET, "127.0.0.1", &serv_addr.sin_addr) <= 0) {
        std::cerr << "Invalid address/ Address not supported" << std::endl;
        return;
    }

    if (connect(sock, (struct sockaddr *)&serv_addr, sizeof(serv_addr)) < 0) {
        std::cerr << "Connection Failed" << std::endl;
        return;
    }

    send(sock, message.c_str(), message.size(), 0);
    close(sock);
}

int main() {
    srand(time(0));
    std::string message, encodedMessage, noisyMessage;

    std::cout << "Enter a message: ";
    std::getline(std::cin, message);

    // Capa de presentación
    std::string binaryMessage = encodeASCII(message);
    std::cout << "Binary message: " << binaryMessage << std::endl;

    // Capa de enlace
    encodedMessage = hammingEncode(binaryMessage);
    std::cout << "Encoded message: " << encodedMessage << std::endl;

    // Capa de ruido (aplicada automáticamente con probabilidad fija)
    noisyMessage = applyNoise(encodedMessage, ERROR_PROBABILITY);
    std::cout << "Noisy message: " << noisyMessage << std::endl;

    // Capa de transmisión
    sendMessage(noisyMessage);

    return 0;
}

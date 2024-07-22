#include <iostream>
#include <vector>
#include <cmath>

// Función para calcular el número de bits de paridad necesarios
int calculateParityBits(int m)
{
    for (int r = 0; r < m; r++)
    {
        if ((m + r + 1) <= std::pow(2, r))
        {
            return r;
        }
    }
    return 0; // En caso de error, aunque no debería ocurrir
}

// Función para codificar un mensaje usando el código de Hamming
std::string hammingEncode(const std::string &data)
{
    int m = data.size();
    int r = calculateParityBits(m);
    int n = m + r;

    std::vector<char> encodedData(n, '0');

    int j = 0;
    for (int i = 1; i <= n; i++)
    {
        if ((i & (i - 1)) == 0)
        {
            encodedData[i - 1] = 'P';
        }
        else
        {
            encodedData[i - 1] = data[j];
            j++;
        }
    }

    for (int i = 0; i < r; i++)
    {
        int parityPos = std::pow(2, i);
        int parity = 0;
        for (int j = 1; j <= n; j++)
        {
            if (j & parityPos)
            {
                parity ^= (encodedData[j - 1] == '1') ? 1 : 0;
            }
        }
        encodedData[parityPos - 1] = (parity == 0) ? '0' : '1';
    }

    return std::string(encodedData.begin(), encodedData.end());
}

int main()
{
    std::string message;
    std::cout << "Enter a binary message: ";
    std::cin >> message;

    std::string encodedMessage = hammingEncode(message);
    std::cout << "Encoded message: " << encodedMessage << std::endl;

    return 0;
}

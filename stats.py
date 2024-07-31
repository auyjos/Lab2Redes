import pandas as pd
import matplotlib.pyplot as plt

# Cargar datos desde el archivo CSV
df = pd.read_csv('hamming_analysis.csv')

# Contar el número de mensajes corregidos y con errores
status_counts = df['Status'].value_counts()

# Graficar la tasa de corrección y errores
plt.figure(figsize=(10, 6))
plt.bar(status_counts.index, status_counts.values, color=['green', 'red'])
plt.xlabel('Status')
plt.ylabel('Number of Messages')
plt.title('Hamming Code Correction Analysis')
plt.savefig('hamming_analysis.png')
plt.show()

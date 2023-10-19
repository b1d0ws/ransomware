import zipfile
import os
import time

zip_file_path = 'Receita.zip'

# Extraindo o arquivo diretamente na pasta atual sem criar outra pasta
extraction_dir = '.'

with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
    zip_ref.extractall(extraction_dir)

# Registrando o tempo atual
extraction_time = time.time()

file_to_check = os.path.join(extraction_dir, 'Receita.exe')

while True:
    if os.path.exists(file_to_check):
        print(f"Checking: {file_to_check}...")
    else:
        # Registrando o tempo de exclusão:
        deletion_time = time.time()
        elapsed_time = deletion_time - extraction_time
        print(f"Tempo entre extração e exclusão: {elapsed_time:.2f} segundos")
        break

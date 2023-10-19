import subprocess
import os
import time

executable_path = 'Receita.exe'

# Registrando o tempo atual
start_time = time.time()
process = subprocess.Popen(executable_path)

process.wait()

file_to_check = 'Receita.exe'

while True:
    if os.path.exists(file_to_check):
        print(f"Checking: {file_to_check}...")
    else:
        # Registrando o tempo de exclusão:
        deletion_time = time.time()
        elapsed_time = deletion_time - start_time
        print(f"Time between execution and deletion: {elapsed_time:.2f} seconds")
        break

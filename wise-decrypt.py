import socket
import string

def xor_strings(s1, s2):
    return ''.join(chr(ord(a) ^ ord(b)) for a, b in zip(s1, s2))

def find_full_key(encoded_hex):
    known_start = "THM{"
    decoded = bytes.fromhex(encoded_hex).decode('latin-1')
    
    key_start = xor_strings(decoded[:4], known_start[:4])
    
    for char in string.ascii_letters + string.digits:
        potential_key = key_start + char
        decrypted = xor_strings(decoded, potential_key * (len(decoded) // len(potential_key) + 1))
        
        if decrypted.startswith("THM{") and decrypted.endswith("}"):
            return potential_key, decrypted

    return None, None

def connect_and_solve(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        
        # Receive the encoded text
        data = s.recv(1024).decode()
        print("Received:", data)
        
        # Extract the encoded hex
        encoded_hex = data.split(": ")[1].strip()
        
        # Find the key and decrypt
        key, decrypted = find_full_key(encoded_hex)
        
        if key:
            print(f"Found key: {key}")
            print(f"Decrypted message: {decrypted}")
            
            # Send the key
            s.sendall(f"{key}\n".encode())
            
            # Receive the response
            response = s.recv(1024).decode()
            print("Server response:", response)
        else:
            print("Couldn't find a valid key.")

# Server details
HOST = '10.10.158.250'  # Replace with the actual IP if different
PORT = 1337

# Run the script
connect_and_solve(HOST, PORT)

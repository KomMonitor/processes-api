from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

print("Generiere RSA-Schlüsselpaar...")

# 1. Privaten Schlüssel erzeugen (2048 Bit)
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048
)

# 2. Privaten Schlüssel im PEM-Format formatieren
pem_private = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
)

# 3. Öffentlichen Schlüssel extrahieren und formatieren
pem_public = private_key.public_key().public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

# 4. In Dateien schreiben
with open("processor/processes_private_key.pem", "wb") as f:
    f.write(pem_private)

with open("processes_public_key.pem", "wb") as f:
    f.write(pem_public)

print("Success! 'processes_private_key.pem' und 'processes_public_key.pem' are created.")
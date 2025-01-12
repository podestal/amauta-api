from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization
import base64

def generate_vapid_keys():
    private_key = ec.generate_private_key(ec.SECP256R1())
    public_key = private_key.public_key()

    private_key_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    public_key_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    # Convert public key to URL-safe Base64 format
    public_key_b64 = base64.urlsafe_b64encode(public_key_bytes).decode("utf-8").rstrip("=")

    return private_key_pem.decode("utf-8"), public_key_b64

private_key, public_key = generate_vapid_keys()
print("VAPID Private Key:", private_key)
print("VAPID Public Key:", public_key)

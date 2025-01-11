from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization
from django.core.management.base import BaseCommand
import base64

class Command(BaseCommand):
    help = "Generate VAPID public and private keys"

    def handle(self, *args, **kwargs):
        # Generate private key
        private_key = ec.generate_private_key(ec.SECP256R1())
        private_key_bytes = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        private_key_b64 = base64.urlsafe_b64encode(private_key_bytes).decode('utf-8')

        # Generate public key
        public_key = private_key.public_key()
        public_key_bytes = public_key.public_bytes(
            encoding=serialization.Encoding.X962,
            format=serialization.PublicFormat.UncompressedPoint
        )
        public_key_b64 = base64.urlsafe_b64encode(public_key_bytes).decode('utf-8')

        self.stdout.write(f"Public Key: {public_key_b64}")
        self.stdout.write(f"Private Key: {private_key_b64}")
import subprocess

class WireguardConfig:

    def generate_wg_keypair() -> tuple[str, str]:
        private_key_bytes = subprocess.run(["wg", "genkey"], capture_output=True).stdout
        public_key_bytes = subprocess.run(["wg", "pubkey"], input=private_key_bytes, capture_output=True).stdout
        return private_key_bytes.decode("utf-8").strip(), public_key_bytes.decode("utf-8").strip()
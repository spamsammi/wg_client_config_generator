import click
from src.wg.WireguardConfig import WireguardConfig

@click.command()
@click.option("-a", "--address", type=str, required=True, help="The address of the client")
@click.option("-i", "--interface", type=str, required=False, default="wg0", help="The wireguard server interface name (default: wg0)")
@click.option("-q", "--qr", is_flag=True, help="Whether to generate a QR code for the client config")
@click.option("-s", "--stdout", is_flag=True, help="Whether to print the client config to stdout")
@click.option("-f", "--file", type=str, required=False, default=None, help="Save the client config to a file")
@click.option("-e", "--email", type=str, required=False, default=None, help="Send the client config to an email address")


def generate_wg_config(address: str, interface: str, qr: bool, stdout: bool, file: str | None, email: str | None):
    private_key, public_key = WireguardConfig.generate_wg_keypair()
    print(private_key, public_key)

if __name__ == "__main__":
    generate_wg_config()

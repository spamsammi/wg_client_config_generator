import os
import click
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, Template
from src.wg.WireguardConfig import WireguardConfig
from src.util.ConfigDelivery import ConfigDelivery

def render_template(template_file: str, address: str, private_key: str, public_key: str) -> Template:
    try:
        template_dir = Path.home() / ".config" / "wg_client_config_generator" / "templates"
        # If the template is not in the default template directory, whatever path was given
        if not Path(template_dir / template_file).exists():
            template_dir, template_file = os.path.split(template_file)
            # Check if this new path exists, then error out if not
            if not Path(template_dir / template_file).exists():
                raise FileNotFoundError(f"Template {template_file} not found")
        env = Environment(loader=FileSystemLoader(template_dir))
        template = env.get_template(template_file)
        return template.render(address=address, privatekey=private_key, publickey=public_key)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return None

@click.command()
@click.option("-a", "--address", type=str, required=True, help="The address of the client")
@click.option("-i", "--interface", type=str, required=False, default="wg0", help="The wireguard server interface name (default: wg0)")
@click.option("-t", "--template", type=str, required=False, default="wg0.conf.jinja2", help="The template to use for the client config; defaults to the relative templates in ~/.config/wg_client_config_generator/templates")
@click.option("-q", "--qr", is_flag=True, required=False, default=False, help="Generate a QR code for the client config; prints to stdout unless file or email is provided")
@click.option("-c", "--config", is_flag=True, required=False, default=False, help="Generate the client config; prints to stdout unless file or email is provided")
@click.option("-f", "--file", is_flag=True, required=False, default=False, help="Save the client config to a file")
@click.option("-e", "--email", type=str, required=False, default=None, help="Send the client config to an email address")
@click.option("-p", "--print-output", is_flag=True, required=False, default=False, help="Print the QR code and/or client config to stdout regardless of other options")
def main(address: str, interface: str, template: str, qr: bool, config: bool, file: bool, email: str | None, print_output: bool):
    private_key, public_key = WireguardConfig.generate_wg_keypair()
    client_config = render_template(template, address, private_key, public_key)
    config_delivery = ConfigDelivery(client_config, address=address, qr=qr, config=config, file=file, email=email, print_output=print_output)
    config_delivery.deliver()

if __name__ == "__main__":
    main()

import os
import click
from src.wg.WireguardConfig import WireguardConfig
from jinja2 import Environment, FileSystemLoader, Template

@click.command()
@click.option("-a", "--address", type=str, required=True, help="The address of the client")
@click.option("-i", "--interface", type=str, required=False, default="wg0", help="The wireguard server interface name (default: wg0)")
@click.option("-t", "--template", type=str, required=False, default="templates/default.jinja2", help="The template to use for the client config (default: templates/default.jinja2)")
@click.option("q", "qr", is_flag=True, required=False, default=False, help="Generate a QR code for the client config; prints to stdout unless file or email is provided")
@click.option("c", "config", is_flag=True, required=False, default=False, help="Generate the client config; prints to stdout unless file or email is provided")
@click.option("f", "file", is_flag=True, required=False, default=False, help="Save the client config to a file")
@click.option("e", "email", type=str, required=False, default=None, help="Send the client config to an email address")
@click.option("p", "print", is_flag=True, required=False, default=False, help="Print the QR code and/or client config to stdout regardless of email or file options")

def render_template(template_path: str, **kwargs) -> Template:
    template_dir, template_file = os.path.split(template_path)
    env = Environment(loader=FileSystemLoader(template_dir or os.getcwd()))
    template = env.get_template(template_file)
    return template.render(**kwargs)

def generate_wg_config(address: str, interface: str, template: str, qr: bool, stdout: bool, file: str | None, email: str | None):
    private_key, public_key = WireguardConfig.generate_wg_keypair()
    print(private_key, public_key)

if __name__ == "__main__":
    generate_wg_config()

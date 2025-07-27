import os
from pathlib import Path


class Initialize:

    if __name__ == "__main__":
        # Create config directory if it doesn't exist
        config_dir = Path.home() / ".config" / "wg_client_config_generator"
        if not config_dir.exists():
            config_dir.mkdir(parents=True, exist_ok=True)
            print(f"Config directory created: {config_dir}")

        # Create templates directory if it doesn't exist and create default semi-minimal template
        templates_dir = config_dir / "templates"
        if not templates_dir.exists():
            templates_dir.mkdir(parents=True, exist_ok=True)
            with open(templates_dir / "wg0.conf.jinja2", "w") as f:
                f.write("""[Interface]
Address = {{address}}
PrivateKey = {{privatekey}}

[Peer]
PublicKey = {{publickey}}""")
        print(f"Templates directory created: {templates_dir}")

        # Create configs directory if it doesn't exist
        configs_dir = config_dir / "configs"
        if not configs_dir.exists():
            configs_dir.mkdir(parents=True, exist_ok=True)
            print(f"Configs directory created: {configs_dir}")
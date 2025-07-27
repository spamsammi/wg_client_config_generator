import qrcode
from pathlib import Path

class ConfigDelivery:

    def __init__(self, client_config: str, **kwargs):
        self.client_config = client_config
        self.address = kwargs.get("address")
        self.qr = kwargs.get("qr")
        self.config = kwargs.get("config")
        self.file = kwargs.get("file")
        self.email = kwargs.get("email")
        self.print_output = kwargs.get("print_output")
        self.__default_delivery()

    def __default_delivery(self):
        # If nothing is provided, set qr to True to display the qr code to the screen
        if not self.qr and not self.config and not self.file and not self.email:
            self.qr = True
            self.print_output = True
        # If qr is provided, and file or email are not, set print to True
        if self.qr and not self.file and not self.email:
            self.print_output = True
        # If config is provided, and file or email are not, set print to True
        if self.config and not self.file and not self.email:
            self.print_output = True

    def generate_qr_code(self) -> qrcode.QRCode:
        qr = qrcode.QRCode()
        qr.add_data(self.client_config)
        qr.make(fit=True)
        return qr

    def deliver(self):
        if self.qr:
            qr = self.generate_qr_code()
            # Display the qr code to screen if we are not sending to file or email
            if self.print_output:
                qr.print_ascii(invert=True)
        if self.config:
            # Display the client config to screen if we are not sending to file or email
            if (not self.file and not self.email) or self.print_output:
                print(self.client_config)
        if self.file:
            config_dir = Path.home() / ".config" / "wg_client_config_generator" / "configs"
            if self.config:
                with open(config_dir / f"{self.address}.conf", "w") as f:
                    f.write(self.client_config)
                if self.print_output:
                    print(self.client_config)
            if self.qr:
                img = qr.make_image(fill_color="black", back_color="white")
                img.save(config_dir / f"{self.address}.png")
                if self.print_output:
                    qr.print_ascii(invert=True)
        if self.email:
            pass
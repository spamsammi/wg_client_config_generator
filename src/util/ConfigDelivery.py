import os
import qrcode

class ConfigDelivery:

    # src/util/ConfigDelivery.py -> this file
    # ../../configs -> this is the default config directory
    DEFAULT_CONFIG_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "configs")

    def __init__(self, client_config: str, **kwargs):
        self.client_config = client_config
        self.address = kwargs.get("address")
        self.qr = kwargs.get("qr")
        self.config = kwargs.get("config")
        self.file = kwargs.get("file")
        self.email = kwargs.get("email")
        self.print = kwargs.get("print")

    def __default_delivery(self):
        # If nothing is provided, set qr to True to display the qr code to the screen
        if not self.qr and not self.config and not self.file and not self.email:
            self.qr = True
            self.print = True
        # If qr is provided, and file or email are not, set print to True
        if self.qr and not self.file and not self.email:
            self.print = True
        # If config is provided, and file or email are not, set print to True
        if self.config and not self.file and not self.email:
            self.print = True

    def generate_qr_code(self) -> qrcode.QRCode:
        qr = qrcode.QRCode()
        qr.add_data(self.client_config)
        qr.make(fit=True)
        return qr

    def get_file_path(self, file_name: str) -> str:
        return os.path.join(self.DEFAULT_CONFIG_DIR, file_name)

    def delivery(self):
        self.__default_delivery()
        if self.qr:
            qr = self.generate_qr_code()
            # Display the qr code to screen if we are not sending to file or email
            if self.print:
                qr.print_ascii()
        if self.config:
            # Display the client config to screen if we are not sending to file or email
            if (not self.file and not self.email) or self.print:
                print(self.client_config)
        if self.file:
            if self.config:
                with open(self.get_config_path(f"{self.address}.conf"), "w") as f:
                    f.write(self.client_config)
                if self.print:
                    print(self.client_config)
            if self.qr:
                img = qr.make_image(fill_color="black", back_color="white")
                img.save(self.get_config_path(f"{self.address}.png"))
                if self.print:
                    qr.print_ascii()
        if self.email:
            pass
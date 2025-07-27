import string
import secrets
import qrcode
import tempfile
import zipfile
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

    def __generate_qr_code(self) -> qrcode.QRCode:
        qr = qrcode.QRCode()
        qr.add_data(self.client_config)
        qr.make(fit=True)
        return qr

    def __generate_random_password(self, length: int = 10) -> str:
        alphabet = string.ascii_letters + string.digits + string.punctuation
        return ''.join(secrets.choice(alphabet) for _ in range(length))

    def __file_name_format(self, name: str) -> str:
        return name.replace(".", "_").replace("/", "_")
    
    def __create_config_file(self, path: Path, name: str, config: str):
        with open(path / f"{self.__file_name_format(name)}.conf", "w") as f:
            f.write(config)

    def __create_qr_code_file(self, path: Path, name: str, qr: qrcode.QRCode):
        img = qr.make_image(fill_color="black", back_color="white")
        img.save(path / f"{self.__file_name_format(name)}.png")

    # This encyprtion is not very secure, but it's good enough for our use case to just temporarily transfer the config files via email
    def __create_zip_file(self, path: Path) -> (str, str):
        password = self.__generate_random_password()
        zip_file_name = f"{self.__file_name_format(self.address)}.zip"
        with zipfile.ZipFile(path / zip_file_name, "w", compression=zipfile.ZIP_DEFLATED) as zf:
            zf.setpassword(password.encode())
            for file in Path(path).iterdir():
                if file.is_file() and file.name != zip_file_name:
                    zf.write(file, arcname=file.name)
        return password, path / zip_file_name


    def deliver(self):
        if self.qr:
            qr = self.__generate_qr_code()
            if self.print_output:
                print("Client QR Code:")
                qr.print_ascii(invert=True)
        if self.config:
            if self.print_output:
                print("Client Config:")
                print(self.client_config)
        if self.file:
            config_dir = Path.home() / ".config" / "wg_client_config_generator" / "configs"
            if self.config:
                self.__create_config_file(config_dir, self.address, self.client_config)
            if self.qr:
                self.__create_qr_code_file(config_dir, self.address, qr)
        # For email, files will always be be encrypted and the password separated from the actual email
        if self.email:
            with tempfile.TemporaryDirectory() as temp_dir:
                temp_dir = Path(temp_dir)
                if self.config:
                    self.__create_config_file(temp_dir, self.address, self.client_config)
                if self.qr:
                    self.__create_qr_code_file(temp_dir, self.address, qr)
                password, path = self.__create_zip_file(temp_dir)
                print(password, path)

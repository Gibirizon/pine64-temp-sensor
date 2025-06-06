import configparser


class Mailer:
    file_path: str

    def __init__(self, file_path):
        self.file_path = file_path
        self.get_config()

    def get_config(self):
        config = configparser.ConfigParser()
        config.read(self.file_path)
        print(config.sections())

    def send_email(self, temperature: float):
        pass

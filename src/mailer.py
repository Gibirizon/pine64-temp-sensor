import configparser
from pathlib import Path
from typing import TypedDict

from src.config import MAIL_SECTION, REQUIRED_MAIL_INFO


class MailInfo(TypedDict):
    sender: str
    password: str
    server: str
    port: int
    recipient: str


class Mailer:
    _file_path: Path
    _mail_info: MailInfo
    _config: configparser.ConfigParser

    def __init__(self, file_path: Path):
        self._file_path = file_path
        self.get_config()
        self.get_and_check_params()

    def get_config(self):
        self._config = configparser.ConfigParser()
        _ = self._config.read(self._file_path)

    def _check_section(self):
        if MAIL_SECTION not in self._config:
            raise ValueError(f"Section {MAIL_SECTION} not found in {self._file_path}")

    def get_and_check_params(self):
        self._mail_info = self._config[MAIL_SECTION]  # pyright: ignore[reportAttributeAccessIssue]
        missing = [x for x in REQUIRED_MAIL_INFO if x not in self._mail_info]
        if len(missing) != 0:
            msg = f"Did not find any values for parameter(s) {', '.join(missing)} in the config file"
            raise ValueError(msg)

    def send_email(self, temperature: float):
        pass

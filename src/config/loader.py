import os
import json
import logging
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("elastic_transport").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)
import logging.config
from dotenv import load_dotenv
from typing import Generic, TypeVar, Any
from abc import ABC, abstractmethod

from configparser import ConfigParser


T = TypeVar('T', bound='LoaderBase')

class LoaderBase(ABC, Generic[T]):
    @abstractmethod
    def load(self) -> T:
        raise NotImplementedError()


class IniFileLoader(LoaderBase[ConfigParser]):
    def __init__(self, file_path: str):
        self.file_path = file_path

    def load(self) -> ConfigParser:
        config = ConfigParser()
        config.read(self.file_path)

        return config


class EnvFileLoader(LoaderBase[bool]):
    def __init__(self, file_path: str):
        self.file_path = file_path

    def load(self) -> bool:
        return load_dotenv(self.file_path)


class JsonFileLoader(LoaderBase[dict[str, Any]]):
    def __init__(self, file_path: str):
        self.file_path = file_path

    def load(self) -> dict[str, Any]:
        with open(self.file_path, 'r') as f:
            return json.load(f)


class InfoFilter(logging.Filter):
    def filter(self, record):
        return record.levelno == logging.INFO


class AboveWarningFilter(logging.Filter):
    def filter(self, record):
        return record.levelno >= logging.WARNING


class ConfigManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(ConfigManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self.CONFIG_FILE_PATH = "./src/config/config.ini"
        self.LOGGER_FILE_PATH = "./src/config/logger.ini"
        self.ENV_FILE_PATH = ".env"
        self.config = None
        self.agent_config = None
        self.kafka_config = None

    def __call__(self):
        self._check_files_exist()
        self._load_env()
        self._load_ini()
        self._setup_logger()

        return self

    def _check_files_exist(self):
        for path in [self.CONFIG_FILE_PATH, self.LOGGER_FILE_PATH, self.ENV_FILE_PATH]:
            if not os.path.exists(path):
                raise FileNotFoundError(f'File: {path} does not exist.')

    def _load_ini(self) -> None:
        self.config = IniFileLoader(self.CONFIG_FILE_PATH).load()

    def _load_agent_config(self) -> None:
        if self.config is None:
            raise RuntimeError("Config not loaded. Call _load_config first.")

        self.agent_config = JsonFileLoader(self.config['agent']['config']).load()
        
    def _load_kafka_config(self) -> None:
        if self.config is None:
            raise RuntimeError("Config not loaded. Call _load_config first.")

        self.kafka_config = JsonFileLoader(self.config['kafka']['config']).load()

    def _load_env(self) -> bool:
        return EnvFileLoader(self.ENV_FILE_PATH).load()

    def _setup_logger(self) -> None:
        os.makedirs(
            self.config['log']['log_dir'],
            mode=0o777,
            exist_ok=True
        )
        logging.config.fileConfig(self.LOGGER_FILE_PATH)

        self.logger = logging.getLogger()
        for handler in self.logger.handlers:
            if handler.name == 'sys':
                handler.addFilter(InfoFilter())
            elif handler.name == 'error':
                handler.addFilter(AboveWarningFilter())

    def get_logger(self) -> logging.Logger:
        if self.logger is None:
            raise RuntimeError("Logger not initialized. Call ConfigManager() first.")
        return self.logger


if __name__ == "__main__":
    pass

import logging
from logging.handlers import RotatingFileHandler
from revolt_hostctl.app.config import Config


LOG_LEVELS = {
    "info": logging.INFO,
    "debug": logging.DEBUG,
    "warning": logging.WARNING,
    "error": logging.ERROR,
    "critical": logging.CRITICAL
}


class Logger:
    def __init__(self, config: Config) -> None:
        self.config = config

        self.level = LOG_LEVELS.get(self.config.log_level.lower(), LOG_LEVELS["info"])
        self.logger = logging.getLogger(self.config.app_name)
        self.logger.setLevel(self.level)
        self.logger.propagate = False

        if not self.logger.handlers:
            formatter = logging.Formatter(
                fmt="[%(asctime)s] [%(levelname)s] %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            )

            if not self.config.log_dir.exists():
                self.config.log_dir.mkdir(parents=True, exist_ok=True)

            log_file = self.config.log_dir / f"{self.config.app_name}.log"

            file_handler = RotatingFileHandler(
                log_file,
                maxBytes=self.config.log_max_bytes,
                backupCount=self.config.log_backup_count,
                encoding="utf-8",
            )
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

            if self.config.log_console:
                stream_handler = logging.StreamHandler()
                stream_handler.setFormatter(formatter)
                self.logger.addHandler(stream_handler)

    def debug(self, msg: str, *args, **kwargs) -> None:
        self.logger.debug(msg, *args, **kwargs)

    def info(self, msg: str, *args, **kwargs) -> None:
        self.logger.info(msg, *args, **kwargs)

    def warning(self, msg: str, *args, **kwargs) -> None:
        self.logger.warning(msg, *args, **kwargs)

    def error(self, msg: str, *args, **kwargs) -> None:
        self.logger.error(msg, *args, **kwargs)

    def critical(self, msg: str, *args, **kwargs) -> None:
        self.logger.critical(msg, *args, **kwargs)

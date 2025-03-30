import logging
from pathlib import Path
from logging.handlers import RotatingFileHandler


def configure_logger(log_dir: Path):
    """配置企业级日志系统"""
    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    )

    # 文件日志（自动轮转）
    file_handler = RotatingFileHandler(
        filename=log_dir / "test_run.log",
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=5,
        encoding="utf-8"
    )
    file_handler.setFormatter(formatter)

    # 控制台日志
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # 根日志配置
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)

    # 第三方库日志抑制
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("selenium").setLevel(logging.WARNING)
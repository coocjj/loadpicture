# config/settings.py
"""
全局配置管理中心
功能：多环境配置加载、敏感信息处理、路径管理
"""

import os
import sys
from pathlib import Path
from typing import Dict, Any, Optional
import yaml
from dotenv import load_dotenv

# 基础路径配置
BASE_DIR = Path(__file__).resolve().parent.parent
ENV_FILE = BASE_DIR / ".env"

# 加载环境变量
load_dotenv(ENV_FILE)


class ConfigManager:
    """多环境配置管理器"""

    def __init__(self, env: str = "dev"):
        """
        初始化配置
        :param env: 运行环境 (dev|test|prod)
        """
        self.env = env
        self._config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """加载YAML配置文件并合并环境变量"""
        config_file = BASE_DIR / "config" / f"{self.env}_config.yaml"

        try:
            with open(config_file) as f:
                config = yaml.safe_load(f) or {}
        except FileNotFoundError:
            raise RuntimeError(f"Config file {config_file} not found")

        # 合并环境变量（优先级：环境变量 > YAML配置）
        config.update(self._get_env_vars("APPIUM"))
        return config

    def _get_env_vars(self, prefix: str) -> Dict[str, Any]:
        """获取指定前缀的环境变量"""
        return {
            key[len(prefix) + 1:].lower(): value
            for key, value in os.environ.items()
            if key.startswith(f"{prefix}_")
        }

    @property
    def appium(self) -> Dict[str, Any]:
        """Appium服务器配置"""
        return self._config.get("appium", {})

    @property
    def devices(self) -> Dict[str, Any]:
        """设备配置列表"""
        return self._config.get("devices", {})

    @property
    def android(self) -> Dict[str, Any]:
        """Android平台通用配置"""
        return self._config.get("android", {})

    @property
    def ios(self) -> Dict[str, Any]:
        """iOS平台通用配置"""
        return self._config.get("ios", {})


class PathManager:
    """全局路径管理器"""

    def __init__(self):
        self.artifacts_dir = BASE_DIR / "artifacts"
        self.screenshots_dir = self.artifacts_dir / "screenshots"
        self.reports_dir = self.artifacts_dir / "reports"
        self.logs_dir = self.artifacts_dir / "logs"

        # 自动创建目录
        self._create_directories()

    def _create_directories(self):
        """创建必要目录结构"""
        self.artifacts_dir.mkdir(exist_ok=True)
        self.screenshots_dir.mkdir(exent_ok=True)
        self.reports_dir.mkdir(exist_ok=True)
        self.logs_dir.mkdir(exist_ok=True)

    @property
    def app_path(self) -> Path:
        """待测应用路径"""
        app_name = config_manager.android.get("app_name", "app-debug.apk")
        return BASE_DIR / "apps" / app_name


# ------------------- 初始化配置 -------------------
# 确定运行环境（默认从环境变量获取）
ENVIRONMENT = os.getenv("APPIUM_ENV", "dev").lower()

# 初始化核心组件
config_manager = ConfigManager(ENVIRONMENT)
path_manager = PathManager()

# ------------------- 导出常用配置 -------------------
# Appium 服务配置
APPIUM_SERVER = config_manager.appium.get("host", "http://127.0.0.1:4723")

# 设备默认配置
DEFAULT_DEVICE = config_manager.devices.get("default", {})

# 自动化参数
IMPLICIT_WAIT = config_manager.android.get("implicit_wait", 10)
PAGE_LOAD_TIMEOUT = config_manager.android.get("page_load_timeout", 30)
MAX_RETRY_ATTEMPTS = config_manager.android.get("max_retry", 3)

# 安全敏感信息（从环境变量获取）
API_KEY = os.getenv("API_KEY", "")
TEST_ACCOUNT = {
    "username": os.getenv("TEST_USER", "default_user"),
    "password": os.getenv("TEST_PASS", "secure_pass")
}
#!/usr/bin/env python3
"""
Appium自动化测试执行入口
功能：多设备并行执行、报告生成、异常处理
"""

import argparse
import subprocess
import sys
import yaml
from pathlib import Path
from datetime import datetime
from utils.appium_helper import stop_appium_server, start_appium_server
from config import cfg
# 常量定义
REPORT_DIR = Path(__file__).parent / "reports"
TEST_DIR = Path(__file__).parent / "test_cases"
CONFIG_FILE = Path(__file__).parent / "config" / "devices.yaml"
platformName = cfg.platformName

def load_devices_config():
    """加载多设备配置"""
    with open(CONFIG_FILE) as f:
        config = yaml.safe_load(f)
    return config["devices"]


def parse_arguments(platformName="ios"):
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description='执行Appium自动化测试')
    parser.add_argument('-d', '--device', nargs='+',
                        help='指定设备名称（从devices.yaml中选择）')
    parser.add_argument('-p', '--parallel', type=int, default=0,
                        help='并行进程数（0表示禁用并行）')
    parser.add_argument('-r', '--report', choices=['html', 'allure'], nargs='+',
                        default=['allure'], help='生成测试报告类型')
    if platformName == "ios":
        parser.add_argument('-t', '--tests', default=str(TEST_DIR) + "/" + "test_ios",
                        help='指定测试目录或文件路径')
    else:
        parser.add_argument('-t', '--tests', default=str(TEST_DIR) + "/" + "test_aos",
                            help='指定测试目录或文件路径')
    return parser.parse_args()


def build_pytest_cmd(args, devices,platformName="ios"):
    """构建pytest执行命令"""
    base_cmd = [
        "pytest",
        args.tests,
        "-v",
        "--capture=no",
        "--disable-warnings"
    ]

    # 并行执行配置
    if args.parallel > 0:
        base_cmd.extend(["-n", str(args.parallel), "--dist", "loadscope"])

    # 设备参数化

    if args.device:
        device_params = ["--device={}".format(d) for d in args.device]
        base_cmd.extend(device_params)
    else:
        for d in devices.keys():
            if platformName in d:
                base_cmd.extend(["--device={}".format(d)])
    # 报告生成配置
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    if 'html' in args.report:
        html_report = REPORT_DIR / f"report_{timestamp}.html"
        base_cmd.extend(["--html", str(html_report), "--self-contained-html"])

    if 'allure' in args.report:
        allure_dir = REPORT_DIR / "allure_results"
        allure_dir.mkdir(exist_ok=True)
        base_cmd.extend(["--alluredir", str(allure_dir)])

    return base_cmd


def generate_allure_report():
    """生成Allure报告"""
    allure_results = REPORT_DIR / "allure_results"
    allure_report = REPORT_DIR / "allure_report"

    cmd = [
        "allure", "generate",
        str(allure_results),
        "-o", str(allure_report),
        "--clean"
    ]
    subprocess.run(cmd, check=True)
    print(f"\nAllure报告已生成：file://{allure_report}/index.html")


def main(platformName="ios"):
    # 初始化环境
    args = parse_arguments(platformName)
    devices = load_devices_config()
    REPORT_DIR.mkdir(exist_ok=True)

    try:
        # 启动Appium服务（示例：多设备端口映射）
        # appium_ports = {name: 4723 + i * 2 for i, name in enumerate(devices.keys())}
        # for name, port in appium_ports.items():
        #     start_appium_server(port)

        # 构建并执行测试命令
        pytest_cmd = build_pytest_cmd(args, devices,platformName)
        print("[执行命令]", " ".join(pytest_cmd))
        result = subprocess.run(pytest_cmd)

        # 报告后处理
        if 'allure' in args.report:
            generate_allure_report()

        sys.exit(result.returncode)
    finally:
        stop_appium_server(4723)
        # 清理资源
        # for port in appium_ports.values():
        #     stop_appium_server(port)


if __name__ == "__main__":
    main(platformName)


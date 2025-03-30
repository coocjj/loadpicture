from appium.webdriver import WebElement
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from typing import Tuple


class MobileAutomator:
    def __init__(self, appium_driver):
        """
        初始化移动端自动化控制器
        :param driver: Appium WebDriver实例
        :param platform: 平台类型 ('android'/'ios')
        """
        self.driver = appium_driver

    # ----------------- 基础操作封装 -----------------
    def click(self, locator: Tuple[str, str], timeout: int = None):
        """增强版点击操作"""
        element = self._wait_for_element(locator, timeout)
        try:
            element.click()
        except Exception as e:
            raise Exception(f"Click failed on {locator}: {str(e)}")

    def input_text(self, locator: Tuple[str, str], text: str, timeout: int = None):
        """安全文本输入"""
        element = self._wait_for_element(locator, timeout)
        self._highlight_element(element)
        try:
            element.clear()
            element.send_keys(text)
        except Exception as e:
            raise Exception(f"Input failed on {locator}: {str(e)}")


    def long_press(self, locator: Tuple[str, str], duration: int = 2000):
        """长按操作"""
        element = self._wait_for_element(locator)
        self.driver.tap([(element.location['x'], element.location['y'])], duration)

    # ----------------- 系统交互 -----------------
    def handle_permission_popup(self, allowed: bool = True):
        """处理系统权限弹窗（需根据具体APP调整）"""
        if self.platform == 'android':
            if allowed:
                self.click(('id', 'com.android.packageinstaller:id/permission_allow_button'))
            else:
                self.click(('id', 'com.android.packageinstaller:id/permission_deny_button'))
        elif self.platform == 'ios':
            # iOS弹窗处理需要借助bundle id
            self.driver.switch_to.alert.accept() if allowed else self.driver.switch_to.alert.dismiss()

    # ----------------- 断言方法 -----------------
    def assert_element_present(self, locator: Tuple[str, str], timeout: int = 10):
        """验证元素存在"""
        if not self.is_element_present(locator, timeout):
            raise AssertionError(f"Element {locator} not found")

    def assert_text_in_element(self, locator: Tuple[str, str], expected_text: str):
        """验证元素包含指定文本"""
        element = self._wait_for_element(locator)
        actual_text = element.text
        if expected_text not in actual_text:
            raise AssertionError(f"Expected text '{expected_text}' not found. Actual: '{actual_text}'")

    # ----------------- 实用工具方法 -----------------
    def _wait_for_element(self, locator: Tuple[str, str], timeout: int = None) -> WebElement:
        """等待元素可见并返回"""
        timeout = timeout or self._default_wait_time
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
        except TimeoutException:
            raise NoSuchElementException(f"Element {locator} not found within {timeout}s")

    def rotate_screen(self, orientation: str):
        """旋转屏幕方向"""
        valid_orientations = ['LANDSCAPE', 'PORTRAIT']
        if orientation.upper() not in valid_orientations:
            raise ValueError(f"Invalid orientation. Valid values: {valid_orientations}")
        self.driver.orientation = orientation.upper()

    # ----------------- 元素状态检查 -----------------
    def is_element_present(self, locator: Tuple[str, str], timeout: int = 5) -> bool:
        """检查元素是否存在"""
        try:
            self._wait_for_element(locator, timeout)
            return True
        except NoSuchElementException:
            return False

    def is_element_visible(self, locator: Tuple[str, str]) -> bool:
        """检查元素是否可见"""
        try:
            return self._wait_for_element(locator, 1).is_displayed()
        except (NoSuchElementException, TimeoutException):
            return False

    # ----------------- 页面导航 -----------------
    def navigate_back(self):
        """物理返回键/导航返回"""
        if self.platform == 'android':
            self.driver.press_keycode(self._back_button_key)
        else:
            self.click(('accessibility id', 'Back'))



    def restart_app(self, post_launch_wait: int = 5, reset_strategy: str = 'full', **launch_args):
        """
        iOS应用重启完整实现
        :param post_launch_wait: 启动后等待时间（秒）
        :param reset_strategy: 重置策略
               'basic' - 简单重启
               'full'  - 完全重置（默认）
        :param launch_args: 额外的启动参数
        """

        try:
            # 执行预重启清理
            if reset_strategy == 'full':
                self._pre_restart_cleanup()

            # 终止应用并重置状态
            self.driver.close_app()
            # 处理不同重置策略
            if reset_strategy == 'full':
                self.driver.reset()

            # 重新启动应用
            self.driver.launch_app(**launch_args)
            # 等待应用准备就绪
            time.sleep(post_launch_wait)

            return True
        except Exception as e:
            raise RuntimeError(f"应用重启失败: {str(e)}") from e

    def _pre_restart_cleanup(self):
        """执行重启前的状态清理"""
        try:
            # 清除应用数据（需要启用appium的fullReset能力）
            self.driver.execute_script('mobile: clearKeychains')
        except Exception as e:
            pass



from appium_helper.mobileHandle import MobileAutomator
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait


class LoginPage:
    def __init__(self, appium_driver):
        self.driver = appium_driver
        self.wait = WebDriverWait(appium_driver, 1)

    # 元素定位器（维护在此处）
    _username_field = (AppiumBy.ID, "新机市场")
    _username_target = (AppiumBy.ID, "品牌百科")

    def click_continue(self):
        """点击继续按钮"""
        # self.driver.find_element(*self._username_target).click()
        MobileAutomator(self.driver).click(self._username_field,10)


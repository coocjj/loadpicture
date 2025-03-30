import time

from appium.webdriver.common.appiumby import AppiumBy

from page_objects.iosPage.login_ios_page import LoginPage
from appium_helper.swipeHelper import swipe_element
from appium_helper.mobileHandle import MobileAutomator

class TestLogin:
    def test_login(self, appium_driver):
        # swipe_element(appium_driver,LoginPage._username_target,10)
        login_page = LoginPage(appium_driver)
        login_page.click_continue()
        MobileAutomator(appium_driver).assert_element_present(login_page._username_target,5)



import time

from appium.webdriver.common.appiumby import AppiumBy
import allure
from page_objects.iosPage.login_ios_page import LoginPage
from appium_helper.swipeHelper import swipe_element
from appium_helper.mobileHandle import MobileAutomator

@allure.epic("移动端测试")
@allure.feature("登录模块")
class TestLogin:
    @allure.title("测试用户正常登录")
    @allure.story("验证用户使用正确账号密码登录")
    def test_login(self, appium_driver):
        # swipe_element(appium_driver,LoginPage._username_target,10)
        login_page = LoginPage(appium_driver)
        with allure.step("输入用户名"):
            login_page.click_continue()
        with allure.step("点击登录"):
            MobileAutomator(appium_driver).assert_element_present(login_page._username_target,5)
        with allure.step("验证通过截图"):
            allure.attach(appium_driver.get_screenshot_as_png(), name="登录页面截图",
                          attachment_type=allure.attachment_type.PNG)



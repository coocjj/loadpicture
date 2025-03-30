from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def w3c_swipe(appium_driver,direction, percent=0.6):
            """基于 W3C 协议的滑动
            :param percent: 滑动距离比例 (0-1)
            """
            size = appium_driver.get_window_size()
            actions = ActionChains(appium_driver)

            if direction in ('up', 'down'):
                distance = size['height'] * percent
                if direction == 'up':
                    y_start = size['height'] * 0.8
                    y_end = y_start - distance
                else:
                    y_start = size['height'] * 0.2
                    y_end = y_start + distance
                x = size['width'] // 2

                actions.w3c_actions.pointer_action.move_to_location(x, y_start)
                actions.w3c_actions.pointer_action.pointer_down()
                actions.w3c_actions.pointer_action.move_to_location(x, y_end)

            elif direction in ('left', 'right'):
                distance = size['width'] * percent
                if direction == 'left':
                    x_start = size['width'] * 0.8
                    x_end = x_start - distance
                else:
                    x_start = size['width'] * 0.2
                    x_end = x_start + distance
                y = size['height'] // 2

                actions.w3c_actions.pointer_action.move_to_location(x_start, y)
                actions.w3c_actions.pointer_action.pointer_down()
                actions.w3c_actions.pointer_action.move_to_location(x_end, y)

            actions.w3c_actions.pointer_action.release()
            actions.perform()

def swipe_element(appium_driver,locator,times):
    for i in range(times):
        try:
            element = WebDriverWait(
                appium_driver,
                0.5,
            ).until(EC.presence_of_element_located(locator))
            if element.is_displayed():
                break
        except:
            w3c_swipe(appium_driver, "up", 0.1)












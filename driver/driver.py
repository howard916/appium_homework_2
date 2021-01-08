from appium import webdriver
from appium.webdriver.webdriver import WebDriver


class App:
    _driver: WebDriver = None

    @classmethod
    def start(cls):
        if cls._driver is None:
            caps = {}
            caps["platformName"] = "Android"
            caps["deviceName"] = "emulator-5554"
            caps["appPackage"] = "com.xueqiu.android"
            caps["appActivity"] = ".view.WelcomeActivityAlias"
            caps["noReset"] = "True"
            cls._driver = webdriver.Remote("http://127.0.0.1:4723/wd/hub", caps)
            cls._driver.implicitly_wait(5)
        else:
            cls._driver.launch_app()

        return cls


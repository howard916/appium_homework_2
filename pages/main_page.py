from .basepage import BasePage

class MainPage(BasePage):
    def goto_me(self):
        self.find_ele(['xpath', '//*[@resource-id="android:id/tabs"]//*[@text="我的"]']).click()
        return self

    def mock_pop_window(self):
        self.find_ele(['xpath', '//*[@resource-id="com.xueqiu.android:id/post_status"]']).click()
        return self

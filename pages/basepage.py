import re
import yaml
from .black_list import handle_exception
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from driver import App
import os

file_path = os.path.dirname(os.path.abspath(__file__))


class BasePage(App):
    @handle_exception
    def find_ele(self, by: list):
        return self._driver.find_element(*by)

    def find_eles(self, by: list):
        return self._driver.find_elements(*by)

    def wait_until(self, by: list, wait_type='view'):
        # 加快定位速度, 但同时也保证速度不至于过快
        self._driver.implicitly_wait(1)
        try:
            if wait_type == 'view':
                return WebDriverWait(self._driver, 3).until(ec.visibility_of_element_located(by))
            elif wait_type == 'click':
                return WebDriverWait(self._driver, 5).until(ec.element_to_be_clickable(by))
            elif wait_type == 'exist':
                # xpath 和 css方式不支持直接在page source中查找
                if by[0] == 'xpath' or by[0] == 'css selector':
                    return WebDriverWait(self._driver, 5).until(ec.presence_of_element_located(by))
                else:
                    return WebDriverWait(self._driver, 5).until(lambda driver: by[1] in driver.page_source)
            else:
                print(f': not except wait_type -> {wait_type}')
                raise

        except TimeoutException:
            self._save_page_source()

        finally:
            self._driver.implicitly_wait(5)

    def _ui_scroll_find_ele(self, by: list):  # 官方使用uiautomator定位方式
        print(': 执行UI滚动查询')
        by_name = None
        get_by = by[:]
        if get_by[0] == 'id':
            by_name = 'resourceId'
            get_by[1] = self._driver.current_package + ':id/' + get_by[1]

        if get_by[0] == 'class name':
            by_name = 'className'

        if get_by[0] == 'xpath':
            try:
                if "@text" in get_by[1]:
                    mo = re.search(r"@text=[\'\"](.*)[\'\"]", get_by[1], re.M | re.I)
                    get_by[1] = mo.groups()[0]
                    by_name = 'text'
                else:
                    print(': when using xpath to scroll find eles, it only supports "text()" attribute')
            except Exception as e:
                print(f': ui_scroll_find error {e.__class__.__name__}')

        if get_by[0] == 'name':
            by_name = 'text'

        ele_find = None
        if by_name is not None:
            cmd = 'new UiScrollable(new UiSelector().scrollable(true)' \
                  '.instance(0)).scrollIntoView(new UiSelector()' \
                  f'.{by_name}("{get_by[1]}").instance(0));'
            try:
                ele_find = self._driver.find_element_by_android_uiautomator(cmd)
            except:
                pass

            if ele_find:
                print(':Scroll find ele success')
            else:
                print(':Scroll cannot find ele')

        else:
            ele_find = None

        return ele_find

    def toast_actions(self, t_type='view'):
        toast_ele = ['xpath', '//*[@class="android.widget.Toast"]']

        def get_text():
            if is_exist():
                return self.find_ele(toast_ele).text
            else:
                return False

        def is_exist():
            if self.find_eles(toast_ele):
                return True
            else:
                return False

        if t_type == 'view':
            return is_exist()
        else:
            return get_text()

    def _save_page_source(self):
        page_source = self._driver.page_source
        with open(f'{file_path}/page_source.xml', 'w', encoding='utf-8') as f:
            f.write(page_source)

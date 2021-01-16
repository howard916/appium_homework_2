import yaml
import os
import logging
from selenium.common.exceptions import NoSuchElementException

file_path = os.path.dirname(os.path.abspath(__file__))


def handle_exception(func):
    def run(*args, **kwargs):
        self = args[0]
        try:
            return func(*args, **kwargs)

        except NoSuchElementException:
            # 异常处理机制
            self._driver.implicitly_wait(1)

            # 截图方法
            self.allure_screenshot('未找到元素, 当前截图')

            # 遍历黑名单, 如果存在则执行点击操作
            black_list = yaml.safe_load(open(f'{file_path}/black_list.yaml'))
            for b_ele in black_list:
                eles = self.find_eles(b_ele)
                if len(eles) >= 1:
                    eles[0].click()

            return func(*args, **kwargs)

        except Exception as e:
            raise e

        finally:
            # 恢复隐式等待5s
            self._driver.implicitly_wait(5)

    return run

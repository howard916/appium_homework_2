import yaml
import os

file_path = os.path.dirname(os.path.abspath(__file__))


def handle_exception(func):
    def run(*args, **kwargs):
        func_self = args[0]
        try:
            return func(*args, **kwargs)

        except:
            # 异常处理机制
            func_self._driver.implicitly_wait(0)

            # 遍历黑名单, 如果存在则执行点击操作
            black_list = yaml.safe_load(open(f'{file_path}/black_list.yaml'))
            for b_ele in black_list:
                eles = func_self.find_eles(b_ele)
                if len(eles) >= 1:
                    eles[0].click()

            # ui滚动查询方法
            print(':Start scroll find')
            func_self._ui_scroll_find_ele(args[1])

            # 恢复隐式等待5s
            func_self._driver.implicitly_wait(5)

            return func(*args, **kwargs)

    return run

    # 为了加快判定速度(在find_ele中已经执行过隐式等待5s), 在执行黑名单前默认将隐式等待设置为0

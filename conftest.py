from driver import App
import pytest
import allure
import os

file_path = os.path.dirname(os.path.abspath(__file__))

@pytest.fixture(scope='session', autouse=True)
def start():
    App().start()


@pytest.fixture(scope='class', autouse=True)
def screen_video():
    os.system(f'scrcpy -r {file_path}/temp/screen_video.mp4 &')
    yield
    os.system('killall scrcpy')
    allure.attach(open(f'{file_path}/temp/screen_video.mp4', 'rb').read(), name="屏幕录制",
                  attachment_type=allure.attachment_type.MP4)

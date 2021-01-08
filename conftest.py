from driver import App
import pytest


@pytest.fixture(scope='session', autouse=True)
def start():
    App().start()

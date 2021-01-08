from pages import MainPage

class TestBlackList:
    def test_blacklist(self):
        MainPage().mock_pop_window().goto_me()

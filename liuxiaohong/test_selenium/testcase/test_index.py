from test_selenium.page.index import Index


class TestIndex:

    def setup(self):
        self.index = Index()

    def test_register(self):
        self.index.goto_register().register("测试刘小红")

    def test_login(self):
        register_page = self.index.goto_login().goto_regitstry().register("测试哈哈")
        error = register_page.get_error_message()
        print(error)
        assert "请选择" in "|".join(error)

    def teardown(self):
        self.index.close()

import pytest

from test_requests.api.base_api import BaseApi
from test_requests.api.tag import Tag


class TestTag:
    data = BaseApi.yaml_load("../data/test_tag.data.yaml")
    steps = BaseApi.yaml_load("../data/test_tag.step.yaml")

    @classmethod
    def setup_class(cls):
        cls.tag = Tag()
        cls.reset()

    def test_get(self):
        r = self.tag.get()

        assert r["errcode"] == 0
        print(self.tag.jsonpath(f"$..tag[?(@name !='')]"))

    def test_add(self):
        r = self.tag.add("demo1")
        assert r["errcode"] == 0

    @pytest.mark.parametrize("name", data["test_delete"])
    def test_delete(self, name):
        # 如果有就删除
        r = self.tag.get()
        x = self.tag.jsonpath(f"$..tag[?(@.name=='{name}')]")
        if isinstance(x, list) and len(x) > 0:
            self.tag.delete(tag_id=[x[0]['id']])

        # 环境干净后开始测试
        r = self.tag.get()
        path = "$..tag[?(@.name!='')]"
        size = len(self.tag.jsonpath(path))

        # 添加新标签
        self.tag.add(name)
        r = self.tag.get()
        assert len(self.tag.jsonpath(path)) == size + 1
        tag_id = self.tag.jsonpath(f"$..tag[?(@.name=='{name}')]")[0]['id']
        print(tag_id)
        # 删除新标签
        self.tag.delete(tag_id=[tag_id])

        # 断言
        r = self.tag.get()
        assert len(self.tag.jsonpath(path)) == size


    @pytest.mark.parametrize("name", data["test_delete"][0:1])
    def test_delete_steps(self, name):
        self.tag.params = {"name": name}
        self.tag.step_run(self.steps['test_delete'])

    def teardown(self):
        self.reset()

    @classmethod
    def reset(cls):
        cls.tag.get()
        for name in ["demo1","demo2"]:
            x = cls.tag.jsonpath(f"$..tag[?(@.name=='{name}')]")
            if isinstance(x, list) and len(x) > 0:
                cls.tag.delete(tag_id=[x[0]['id']])

from test_requests.api.wework import WeWork


class Tag(WeWork):
    secret = 'heLiPlmyblHRiKAgGWZky4-KdWqu1V22FeoFex8RfM0'

    def __init__(self):
        self.data = self.api_load("../data/tag.api.yaml")
        # print(self.data)

    # 获取
    def get(self, **kwargs):
        # print(self.data['get'])
        return self.api_send(self.data['get'])

    # 添加
    def add(self, name, **kwargs):
        self.params["name"] = name

        return self.api_send(self.data["add"])

    # 删除
    def delete(self, tag_id=[], group_id=[]):
        self.params["tag_id"] = tag_id
        self.params["group_id"] = group_id

        return self.api_send(self.data["delete"])
import requests

from test_requests.api.base_api import BaseApi


class WeWork(BaseApi):

    token_url = "https://qyapi.weixin.qq.com/cgi-bin/gettoken"
    corpid = 'wwd6da61649bd66fea'

    token = dict()
    token_time = dict()
    secret = "3XBa77sS_W304tGdt-Sc-YManyJ5sKlwq4dSzrIzE_g"

    @classmethod
    def get_token(cls,secret=secret):
        if secret is None:
            return cls.token[secret]

        if secret not in cls.token.keys():
            r = cls.get_access_token(secret)
            cls.token[secret] = r["access_token"]

        return cls.token[secret]

    

    @classmethod
    def get_access_token(cls,secret):
        r = requests.get(
            cls.token_url,
            params={"corpid": cls.corpid, "corpsecret": secret}
        )
        cls.format(r)
        assert r.json()["errcode"] == 0
        return r.json()

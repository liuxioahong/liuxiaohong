import json
import yaml
import requests
from jsonpath import jsonpath

class BaseApi:
    params = {}
    data = {}

    @classmethod
    def format(cls, r):
        cls.r = r
        print(json.dumps(json.loads(r.text), indent=2, ensure_ascii=False))

    def jsonpath(self, path, r=None, **kwargs):
        if r is None:
            r = self.r.json()
        return jsonpath(r, path)

    # 封装yaml 文件加载
    @classmethod
    def yaml_load(cls, path) -> list:
        with open(path,encoding='utf-8') as f:
            return yaml.safe_load(f)

    def api_load(self, path):
        return self.yaml_load(path)

    # 封装requests 请求
    def api_send(self, req: dict):
        print(self.get_token(self.secret))
        req['params']['access_token'] = self.get_token(self.secret)

        # print(req)

        raw = yaml.dump(req)
        for key, value in self.params.items():
            raw = raw.replace(f"${{key}}",repr(value))
            # print("replace")
        req = yaml.safe_load(raw)

        # print(req)

        r = requests.request(
            req['method'],
            url=req['url'],
            params=req['params'],
            json=req['json']
        )

        self.format(r)
        return r.json()

    # 封装类似httprunner，支持步骤
    def step_run(self, steps: list):

        for step in steps:
            raw = yaml.dump(step)
            for key, value in self.params.items():
                raw = raw.replace(f"${{key}}", repr(value))
                # print(raw)
            step = yaml.safe_load(raw)

            if isinstance(step, dict):
                if "method" in step.keys():
                    method = step['method'].split('.')[-1]

                    getattr(self, method)(**step)

                if "extract" in step.keys():
                    self.data[step["extract"]] = getattr(self, 'jsonpath')(**step)

                    # print(self.data[step["extract"]])

                if "assertion" in step.keys():
                    assertion = step["assertion"]
                    if isinstance(assertion, str):
                        assert eval(assertion)

                    if assertion[1] == "eq":
                        assert assertion[0] == assertion[2]
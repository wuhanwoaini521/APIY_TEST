import requests
import json
from utils.log_config import MyLogger
from utils.exceptios import MethodException

logger = MyLogger()


class Base:

    def send_request(self, method, url, headers, body, token=None, files=None):
        """
        发送请求
        :param method: 请求方法
        :param url: 请求地址
        :param headers: 请求头
        :param body: 请求实体
        :param files: 文件
        :return: 响应
        """

        # 处理token
        if "$$token" in headers:
            headers = headers.replace("$$token", token)

        if not isinstance(headers, dict):
            headers = json.loads(headers)
        if not isinstance(body, dict):
            body = json.loads(body)

        if method.upper() == 'GET':
            response = self.get_request(url, headers, body)
        elif method.upper() == 'POST':
            response = self.post_request(url, headers, body, files=files)
        elif method.upper() == 'PUT':
            response = self.put_request(url, headers, body)
        elif method.upper() == 'DELETE':
            response = self.delete_request(url, headers, body)
        else:
            raise MethodException(method)

        return response

    @staticmethod
    def get_request(url, headers, body):
        """
        GET 请求方法
        :return:
        """
        response = requests.get(url=url,
                                headers=headers,
                                params=body)

        response.content.decode('utf-8')

        return response

    @staticmethod
    def post_request(url, headers, body, files=None):
        """
        POST 请求方法
        :return:
        """

        if 'Content-Type' in headers:
            body = json.dumps(body).encode('utf-8')

        response = requests.post(url=url,
                                 headers=headers,
                                 data=body,
                                 files=files)

        response.content.decode('utf-8')

        return response

    @staticmethod
    def put_request(url, headers, body):
        """
        PUT 请求方法
        :return:
        """
        response = requests.put(url=url,
                                headers=headers,
                                params=body)

        response.content.decode('utf-8')

        return response

    @staticmethod
    def delete_request(url, headers, body):
        """
        DELETE 请求方法
        :return:
        """
        response = requests.delete(url=url,
                                   headers=headers,
                                   params=body)

        response.content.decode('utf-8')

        return response


if __name__ == '__main__':
    from utils.read_file import Config_Operation

    con = Config_Operation("../configs/config.ini")
    con_dict = con.get_config("test")

    url = f'{con_dict["host"]}/api/login/userLogin'
    method = 'POST'
    headers = {'Content-Type': 'application/json'}
    body = {
        "username": "admin",
        "password": "123456",
        "loginType": "web"
    }
    request = Base()
    response = request.send_request(url=url,
                                    method=method,
                                    headers=headers,
                                    body=body)

    print(response.json())

    # # get 请求测试
    # response = request.send_request(
    #     url=f'{con_dict["host"]}/api/roles/listRoles',
    #     method="GET",
    #     headers={"Authorization": response.json()["data"]["token"]},
    #     body=""
    # )
    # print(response.json())

"""
用户登录模块验证
"""
import json
import os
import sys
import pytest
import allure

from testCase.test_roles import con_dict
from utils.log_config import MyLogger
from utils.read_file import Handle_Excel, Handle_Txt
from base.baseApi import Base
from utils.asserts import Assert

logger = MyLogger().get_logger()
file_name = "接口测试用例-角色管理.xlsx"
sheet_name = "通用接口-1"
handle_excel = Handle_Excel(file_name, sheet_name)
read_excel = handle_excel.read_excel()
read_txt = Handle_Txt()



@allure.feature(f'{file_name}文件测试用例')
class Test_Roles_Common:

    @allure.story("第一个测试")
    @pytest.mark.parametrize("row, url, method, param", read_excel)
    def test_001_tableAttr(self, row, method, url, param, get_token):
        """
        获取表头信息
        正向用例
        :return:
        :param: 是一个list i： 用例的行数， url： 测试路径， method： 测试方法
        """
        logger.info("开始测试")

        request = Base()
        response = request.send_request(url=url,
                                        method=method,
                                        headers=param[1],
                                        body=param[2], token=get_token)

        text = response.text
        r_json = response.json()  # 接口响应值json
        status_code = response.status_code  # 接口响应结果
        par_code = param[3]  # excel中的响应值
        par = param[4]  # excel中的预期结果

        # print("请求头： ==> ", response.request.headers)

        if Assert().assert_all(r_json, par) == True:
            read_txt.write_txt(file_name, sheet_name, row, 7, "pass", r_json)
        else:
            read_txt.write_txt(file_name, sheet_name, row, 7, "failed", r_json)



if __name__ == '__main__':
    pytest.main(['1test_auth_login.py'])

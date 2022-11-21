"""
用户登录模块验证
"""
import json
import os
import sys
import pytest
import allure

# from testCase.test_roles import con_dict
from utils.log_config import MyLogger
from utils.read_file import Handle_Excel, Handle_Txt
from base.baseApi import Base

logger = MyLogger().get_logger()

file_name = "接口测试用例-角色管理.xlsx"
sheet_name= "通用接口-2"

handle_excel = Handle_Excel(file_name, sheet_name)
read_excel = handle_excel.read_excel()
read_txt = Handle_Txt()


@allure.feature(f'{file_name}文件测试用例')
class Test_Roles_Common2:

    @allure.story("第2个测试")
    @pytest.mark.parametrize("row, url, method, param", read_excel)
    def test_002_2(self, row, method, url, param):
        """
        获取表头信息
        正向用例
        :return:
        """
        logger.info("开始测试")

        request = Base()
        response = request.send_request(url=url,
                                        method=method,
                                        headers=param[1],
                                        body=param[2])

        if response.status_code == param[3]:
            logger.info("测试成功！")
            # 文件写入 json文件，所有用例执行后，进行输入写入excel的操作
            read_txt.write_txt(file_name, sheet_name, row, 7, "pass", response.json())
        else:
            logger.info("测试失败！")
            read_txt.write_txt(file_name, sheet_name, row, 7, "failed", response.json())


if __name__ == '__main__':
    pytest.main(['1test_auth_login.py'])

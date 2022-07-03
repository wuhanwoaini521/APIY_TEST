"""
断言模块
"""

from .log_config import MyLogger
import json


class Assert:

    def __init__(self):
        self.logger = MyLogger()

    def assert_code(self, code, expected_code):
        try:
            assert code == expected_code
            flag = True
        except:
            self.logger.error("statusCode error, expected_code is %s, statusCode is %s " % (expected_code, code))
            flag = False
        else:
            self.logger.info("断言code成功！")
        return flag

    def assert_json(self, text, expected_msg):
        try:
            assert text == json.loads(expected_msg)
            flag = True
        except:
            self.logger.error("Response body msg != expected_msg, expected_msg is %s, body_msg is %s" % (expected_msg, text))
            flag = False
            # raise
        else:
            self.logger.info("断言返回体相等成功！")
        return flag

    def assert_in_json(self, text, expected_msg):
        try:
            assert expected_msg in text
            flag = True
        except:
            self.logger.error("expected_msg not in body!, expected_msg is %s , body_msg is %s" % (expected_msg, text))
            flag = False
            # raise
        return flag

    def assert_all(self, text, expected_msg):
        flag_list = []
        flag = None
        if "@#" not in expected_msg:
            self.logger.info("判断预期结果相等！")
            flag_list.append(self.assert_json(text, expected_msg))
        else:
            self.logger.info("判断预期结果包含！")
            ex_result = expected_msg.split("@#")
            for i in ex_result:
                flag_list.append(self.assert_in_json(json.dumps(text), i))

        self.logger.info("flag_list ==> %s " % flag_list)
        if False in flag_list:
            flag = False
        else:
            flag = True

        return flag
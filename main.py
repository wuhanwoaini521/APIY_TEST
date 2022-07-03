import sys, os
import pytest
from datetime import datetime
from utils.log_config import MyLogger
from time import sleep
from utils.read_file import Handle_Txt, Write_Excel

def main():

    logger = MyLogger().get_logger()
    handle_txt = Handle_Txt()
    handle_excel = Write_Excel()

    logger.info("☆☆☆清除多余的结果文件☆☆☆")
    handle_txt.del_txt()

    # logger = MyLogger()
    nowTime = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    logger.info(f"当前时间为：{nowTime}")

    # 执行用例
    # 生成allure报告 和 html报告
    args = ['--reruns', '0', '--alluredir', f'./outFiles/result/{nowTime}', '--html', f'./outFiles/report/html/{nowTime}.html']

    # 生成pytest-html报告
    # args = ['-s', '--reruns', '1', '--html', './outFiles/report/']
    # 执行pytest测试
    logger.info("☆☆☆开始执行测试☆☆☆")
    pytest.main(args)

    logger = MyLogger().get_logger()
    logger.info("☆☆☆执行结束，生成测试报告☆☆☆")
    sleep(3)
    # 打包生成生成allure报告
    os.system(f'allure generate ./outFiles/result/{nowTime} -o ./outFiles/report/allure/{nowTime} --clean')
    logger.info(f"\n"
                f"报告路径为: \n"
                f"HTML报告 ==> ./outFiles/report/html/{nowTime}.html"
                f"\n"
                f"Allure报告 ==> ./outFiles/report/allure/{nowTime}")

    logger.info("☆☆☆写入Excel测试结果☆☆☆")
    # 写入测试结果（从txt到excel）
    for line in handle_txt.read_txt():
        line = line.split("@#")
        handle_excel.write_excel(line[0], line[1], int(line[2]), int(line[3]), line[5], line[4])


def deal_with_result():
    """
    处理数据，取出报错的用例
    :return:
    """
    pass


if __name__ == '__main__':
    main()

"""
操作数据库封装类
"""
import datetime
import os
import subprocess
import sys

import pymysql
import traceback
from utils.log_config import MyLogger
from utils import con_dict

logger = MyLogger().get_logger()
current_directory = os.path.dirname(os.path.abspath(__file__))
root_path = os.path.abspath(os.path.dirname(current_directory) + os.path.sep + ".")
sys.path.append(root_path)

host = con_dict["db_host"]
username = con_dict["db_username"]
password = con_dict["db_password"]
db = con_dict["db_name"]


class Handle_DB:

    def __init__(self, host, username, password, db, charset='utf8', port=3306):
        self.host = host
        self.username = username
        self.password = password
        self.db = db
        self.charset = charset
        self.port = port

    def connect(self):
        """
        创建数据库连接
        :return:
        """
        try:

            self.conn = pymysql.connect(host=self.host,
                                        port=self.port,
                                        user=self.username,
                                        password=self.password,
                                        db=self.db,
                                        charset=self.charset)

            logger.info("☆☆☆数据库连接成功！☆☆☆")
        except Exception:
            logger.error("数据库连接失败！错误原因：{}".format(traceback.format_exc()))
        else:
            self.cursor = self.conn.cursor()

    def close(self):
        """
        关闭数据库连接
        :return:
        """
        logger.info("☆☆☆数据库连接关闭！☆☆☆")
        self.cursor.close()
        self.conn.close()

    def commit(self):
        """
        提交事务
        :return:
        """
        logger.info("★★★数据提交！★★★")
        self.conn.commit()

    def rollback(self):
        """
        回滚事务
        :return:
        """
        logger.info("★★★数据回滚！★★★")
        self.conn.rollback()

    def __execute(self, sql, params=()):
        try:
            self.connect()
            self.cursor.execute(sql, params)
        except Exception:
            logger.error("sql执行失败！报错原因：{}".format(traceback.format_exc()))
        else:
            return True

    def get_one(self, sql, params=()):
        """
        获取单条数据
        :param sql:
        :param params:
        :return:
        """
        result = None
        try:
            # self.connect()
            # self.cursor.execute(sql, params)
            self.__execute(sql, params)
            result = self.cursor.fetchone()
        except Exception as e:
            logger.error("数据获取失败！报错原因：{}".format(traceback.format_exc()))
        finally:
            self.close()
        return result

    def get_all(self, sql, params=()):
        """
        获取多条数据
        :param sql:
        :param params:
        :return:
        """
        list_data = ()
        try:
            # self.connect()
            # self.cursor.execute(sql, params)
            self.__execute(sql, params)
            list_data = self.cursor.fetchall()
        except Exception as e:
            logger.error("数据获取失败！报错原因：{}".format(traceback.format_exc()))
        finally:
            self.close()
        return list_data

    def delete_one(self, sql, params=()):
        """
        删除一条数据
        :param sql:
        :param params:
        :return:
        """
        result = None
        try:
            # self.connect()
            # self.cursor.execute(sql, params)
            self.__execute(sql, params)
            result = self.cursor.fetchone()

        except Exception as e:
            logger.error("删除数据失败！报错原因：{}".format(traceback.format_exc()))
            self.rollback()
        else:
            self.commit()
        finally:
            self.close()
        return result

    def update_one(self, sql, params=()):
        """
        修改数据
        :param sql:
        :param params:
        :return:
        """
        result = None
        try:
            # self.connect()
            # self.cursor.execute(sql, params)
            self.__execute(sql, params)
            result = self.cursor.fetchone()
        except Exception as e:
            logger.error("修改数据失败！报错原因：{}".format(traceback.format_exc()))
            self.rollback()
        else:
            self.commit()
        finally:
            self.close()
        return result

    # def __del__(self):
    #     self.close()
    #     logger.info("数据库关闭！")

    def backUp_db(self):
        """
        备份数据库
        :param db_name:
        :return:
        """
        # 需要备份到的路径
        today = datetime.datetime.now().strftime("%Y_%m_%d")
        backup_path = root_path + os.path.sep + "backup" + os.path.sep + today
        if not os.path.exists(backup_path):
            os.mkdir(backup_path)
        command = "mysqldump -h%s -u%s -p%s %s | gzip > %s/%s.sql.gz" % (
            self.host, self.username, self.password, self.db, backup_path, self.db)
        print(command)
        exit_code = subprocess.call(command, shell=True)
        # 判断命令是否正常执行，异常则直接抛出
        if exit_code != 0:
            raise Exception('在备份数据库的过程中出错，请检查！')

        print(today)
        print(backup_path)
# class Handle_DB:
#
#     def __init__(self, charset='utf8', port=3306):
#         self.host = host
#         self.username = username
#         self.password = password
#         self.db = db
#         self.charset = charset
#         self.port = port
#
#     def __enter__(self):
#         """
#         创建数据库连接
#         :return:
#         """
#         try:
#
#             self.conn = pymysql.connect(host=self.host,
#                                         port=self.port,
#                                         user=self.username,
#                                         password=self.password,
#                                         db=self.db,
#                                         charset=self.charset)
#             self.cursor = self.conn.cursor()
#             logger.info("数据库连接成功！")
#             return self.cursor
#         except Exception:
#             logger.error("数据库连接失败！错误原因：{}".format(traceback.format_exc()))
#
#     def __exit__(self, exc_type, exc_val, exc_tb):
#         """
#         关闭数据库连接
#         :return:
#         """
#         self.cursor.close()
#         self.conn.close()
#
#     def get_one(self, sql, param=()):
#         with Handle_DB() as db:
#             db.execute(sql, param)
#             result = db.fetchone()
#         return result
#




if __name__ == '__main__':
    host = "192.168.1.200"
    username = "cims"
    password = "cims123$%"
    db = "cims_db"
    my_db = Handle_DB(host=host, username=username, password=password, db=db)

    # # 获取单个
    # sql = 'SELECT * FROM `users`;'
    # result = my_db.get_one(sql)
    # # print("result:{}\n".format(result))
    #
    # print("_"*50)
    #
    # # 获取多个
    # sql = "Select * from `users`;"
    # result = my_db.get_all(sql)
    # # print("result:{}".format(result))
    #
    # for i in result:
    #     print(i)
    my_db.backUp_db()
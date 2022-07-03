from utils.read_file import Config_Operation
import os
import sys


current_directory = os.path.dirname(os.path.abspath(__file__))
root_path = os.path.abspath(os.path.dirname(current_directory) + os.path.sep + ".")
sys.path.append(root_path)

# con = Config_Operation("../../configs/config.ini")

con_path = os.path.join(root_path + os.path.sep + "configs" + os.path.sep + "config.ini")

con = Config_Operation(con_path)
con_dict = con.get_config("test")

if __name__ == '__main__':
    print(con_path)
    print(con_dict)
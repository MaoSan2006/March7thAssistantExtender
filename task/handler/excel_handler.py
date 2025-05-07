import os
import time
import pandas
import logging
import sys

logger = logging.getLogger("process_excel")

class excel_handler:

    @classmethod
    def len_excel(cls):
        if not os.path.exists("account.xlsx"):
            logger.error("未找到account.xlsx文件，请检查文件是否存在")
            sys.exit(1)
        try:
            file = pandas.read_excel("account.xlsx")
            return len(file)
        except Exception as error:
            logger.error(f"读取Excel文件时发生错误")
            logger.error(f"{error}")
            sys.exit(1)

    @classmethod
    def read_excel(cls, row_name, column_name):
        if not os.path.exists("account.xlsx"):
            logger.error("未找到account.xlsx文件，请检查文件是否存在")
            sys.exit(1)
        try:
            file = pandas.read_excel("account.xlsx")
            return file.at[row_name, column_name]
        except Exception as error:
            logger.error(f"读取Excel文件时发生错误")
            logger.error(f"{error}")
            sys.exit(1)

    @classmethod
    def write_excel(cls, row, column, value, retry_time = 0):
        if not os.path.exists("account.xlsx"):
            logger.error("未找到account.xlsx文件，请检查文件是否存在")
            sys.exit(1)
        try:
            file = pandas.read_excel("account.xlsx")
            file.at[row, column] = value
            file.to_excel("account.xlsx", index=False)
            return True
        except PermissionError:
            logger.error("文件被占用，请关闭Excel文件，10秒后自动重试")
            time.sleep(10)
            return cls.write_excel(row, column, value, retry_time + 1) if retry_time <= 6 else False
        except Exception as error:
            logger.error(f"写入Excel文件时发生错误")
            logger.error(f"{error}")
            sys.exit(1)
    
    @classmethod
    def find_column(cls, column_name):
        try:
            file = pandas.read_excel("account.xlsx")
            if column_name in file.columns:
                return True
            else:
                return False
        except Exception as error:
            logger.error(f"读取Excel文件时发生错误")
            logger.error(f"{error}")
            sys.exit(1)
    
    @classmethod
    def write_excel_column(cls, column_name):
        try:
            file = pandas.read_excel("account.xlsx")
            file.insert(len(file.columns), column_name, "")
            file.to_excel("account.xlsx", index=False)
            return True
        except Exception as error:
            logger.error(f"写入Excel文件时发生错误")
            logger.error(f"{error}")
            sys.exit(1)
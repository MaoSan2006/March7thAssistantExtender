import os
import pandas
import logging
import sys

logger = logging.getLogger("process_excel")

class process_excel:

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
    def write_excel(cls, row, column, value):
        if not os.path.exists("account.xlsx"):
            logger.error("未找到account.xlsx文件，请检查文件是否存在")
            sys.exit(1)
        try:
            file = pandas.read_excel("account.xlsx")
            file.at[row, column] = value
            file.to_excel("account.xlsx", index=False)
            return True
        except Exception as error:
            logger.error(f"写入Excel文件时发生错误")
            logger.error(f"{error}")
            sys.exit(1)
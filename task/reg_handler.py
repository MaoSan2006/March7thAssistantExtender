import winreg
import logging
import json
from typing import Dict, Optional
logger = logging.getLogger("reg_Handler")

class reg_handler:

    @classmethod
    def jsondata_decode(cls, json_data):
        json_data = json_data.rstrip(b'\x00').decode('utf-8') #去除\x00结尾标志，并以utf-8解码
        data = json.loads(json_data) #把数据加载到json库中
        return data #返回json格式的数据

    @classmethod
    def jsondata_encode(cls, data):
        data = json.dumps(data, ensure_ascii=False).encode('utf-8') + b'\x00' #加上\x00结尾标志，并以utf-8编码
        return data #返回二进制数据

    @classmethod
    def read_reg_jsondata(cls, reg_root_path, reg_path, reg_name, reg_key):
        logger.debug(f"调用read_reg_jsondata方法，参数: reg_root_path={reg_root_path}, reg_path={reg_path}, reg_name={reg_name}, reg_key={reg_key}")
        try:
            with winreg.OpenKey(reg_root_path, reg_path, 0, winreg.KEY_READ | winreg.KEY_WOW64_64KEY) as key: #注册表键句柄
                data = winreg.QueryValueEx(key, reg_name)[0] #读取数据
                data = cls.jsondata_decode(data) #调用解码函数
                return data.get(reg_key) #返回所需要的值
        except Exception as error:
            logger.error(f"发生未知错误,代码块：读取注册表数据")
            logger.error(f"{error}")

    @classmethod
    def write_reg_jsondata(cls, reg_root_path, reg_path, reg_name, reg_key, reg_values):
        logger.debug(f"调用write_reg_jsondata方法，参数: reg_root_path={reg_root_path}, reg_path={reg_path}, reg_name={reg_name}, reg_key={reg_key}, reg_values={reg_values}")
        try:
            with winreg.OpenKey(reg_root_path, reg_path, 0, winreg.KEY_READ | winreg.KEY_WRITE | winreg.KEY_WOW64_64KEY) as key: #注册表键句柄
                data = winreg.QueryValueEx(key, reg_name)[0] #读取数据
                data = cls.jsondata_decode(data) #调用解码函数
                data[reg_key]= reg_values #修改数据键的值
                data = cls.jsondata_encode(data) #调用编码函数
                winreg.SetValueEx(key, reg_name, 0, winreg.REG_BINARY, data) #写入注册表文件
                return True #返回True为完成
        except Exception as error:
            logger.error(f"发生未知错误,模块：读取注册表数据")
            logger.error(f"{error}")

    @classmethod
    def read_reg_data(cls, reg_root_path, reg_path, reg_name): #关于REG_SZ数据类型的读取
        logger.debug(f"调用read_reg_data方法，参数: reg_root_path={reg_root_path}, reg_path={reg_path}, reg_name={reg_name}")
        try:
            with winreg.OpenKey(reg_root_path, reg_path, 0, winreg.KEY_READ | winreg.KEY_WOW64_64KEY) as key: #注册表键句柄
                data = winreg.QueryValueEx(key, reg_name)[0] #读取数据
                return data #返回数据
        except Exception as error:
            logger.error(f"发生未知错误,代码块：读取注册表数据")
            logger.error(f"{error}")

    @classmethod
    def write_reg_data(cls, reg_root_path, reg_path, reg_name, reg_values): #关于REG_SZ数据类型的写入
        logger.debug(f"调用write_reg_data方法，参数: reg_root_path={reg_root_path}, reg_path={reg_path}, reg_name={reg_name}, reg_values={reg_values}")
        try:
            with winreg.OpenKey(reg_root_path, reg_path, 0, winreg.KEY_READ | winreg.KEY_WRITE | winreg.KEY_WOW64_64KEY) as key: #注册表键句柄
                winreg.SetValueEx(key, reg_name, 0, winreg.REG_SZ, reg_values) #写入注册表文件
                return True #返回True为完成
        except Exception as error:
            logger.error(f"发生未知错误,代码块：写入注册表数据")
            logger.error(f"{error}")
import os
import yaml
import logging

logger = logging.getLogger("get_config")
logger.setLevel(logging.DEBUG)

class config_handler:
    
    @classmethod
    def read(self, key):
        try:
            with open('config.yaml', 'r', encoding = 'utf-8') as file:
                config = yaml.safe_load(file)
                value = config.get(key)
                if value and key.endswith('_path'):
                    return os.path.normpath(value)
                return value
        except FileNotFoundError:
            logging.error(f"未找到config.yaml文件,请检查是否存在或压缩包是否提取完整")
            return None
        except yaml.YAMLError as error_yaml:
            logging.error(f"YAML库错误")
            print(f"{error_yaml}")
            return None
        except KeyError as error:
            logging.error(f"config.yaml文件中未找到{error}参数")
            return None
        except Exception as error:
            logging.error(f"未知错误")
            logging.error(f"{error}")
            return None
            
    @classmethod
    def write(self, key, value):
        try:
            with open('config.yaml', 'r', encoding = 'utf-8') as file:
                config = yaml.safe_load(file)
            config[key] = value
            with open('config.yaml', 'w', encoding = 'utf-8') as file:
                yaml.dump(config, file, allow_unicode = True)
        except FileNotFoundError:
            logging.error(f"未找到config.yaml文件,请检查是否存在或压缩包是否提取完整")
        except yaml.YAMLError as error_yaml:
            logging.error(f"YAML库错误")
            print(f"{error_yaml}")
        except KeyError as error:
            logging.error(f"config.yaml文件中未找到{error}参数")
        except Exception as error:
            logging.error(f"未知错误")
            logging.error(f"{error}")
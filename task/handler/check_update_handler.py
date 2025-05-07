from task.handler.config_handler import config_handler
import requests
import logging

logger = logging.getLogger("check_update_handler")

class check_update:
    @classmethod
    def check_update(cls):
        url = f"https://api.github.com/repos/MaoSan2006/March7thAssistantExtender/releases/latest"
        try:
            response = requests.get(
                url,
                headers = {"Accept": "application/vnd.github.v3+json"},
                timeout = 10
            )
            if response.status_code == 200:
                latest_version = response.json()["tag_name"]
                if latest_version >= config_handler("version"):
                    logger.info(f"发现新版本：{latest_version}")
                    return True
                else:
                    logger.info(f"当前已是最新版本：{latest_version}")
                    return False
            else:
                logger.error(f"获取最新版本失败，状态码：{response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            logger.error(f"检查更新失败：{e}")
            
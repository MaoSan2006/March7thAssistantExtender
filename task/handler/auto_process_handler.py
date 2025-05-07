import pyautogui
import time
import logging
from PIL import Image

logger = logging.getLogger("automatic_operation")
logger.setLevel(logging.DEBUG)

class auto_process_handler:
    @classmethod
    def move(cls, image_path, timeout, confidence = 0.95, more_control_time = 0, more_control_sleep = 0):
        image = image_path
        start_time = time.time()
        logger.debug(f"开始查找{image_path},目标move,最高超时时间{timeout}秒")
        while time.time() - start_time <= timeout:
            try:
                location=pyautogui.center(pyautogui.locateOnScreen(Image.open(image), confidence=confidence))
                pyautogui.moveTo(location)
                while more_control_time > 0:
                    time.sleep(more_control_sleep)
                    more_control_time -= 1
                    pyautogui.moveTo(location)
                    logger.debug(f"已找到[{image_path}]位置并执行【点击】")
                return True
            except FileNotFoundError:
                logger.error(f"未找到{image_path}文件,请检查文件是否存在")
                return False
            except:
                pass
        else:
            logger.debug(f"超时,未找到{image_path}")
            return False

    @classmethod
    def click(cls, image_path, timeout, confidence = 0.95, more_control_time = 0, more_control_sleep = 0):
        image = image_path
        start_time = time.time()
        logger.debug(f"开始查找{image_path},目标click,最高超时时间{timeout}秒")
        while time.time() - start_time <= timeout:
            try:
                location=pyautogui.center(pyautogui.locateOnScreen(Image.open(image), confidence=confidence))
                pyautogui.click(location)
                while more_control_time > 0:
                    time.sleep(more_control_sleep)
                    more_control_time -= 1
                    pyautogui.click(location)
                    logger.debug(f"已找到[{image_path}]位置并执行【点击】")
                return True
            except FileNotFoundError:
                logger.error(f"未找到{image_path}文件,请检查文件是否存在")
                return False
            except:
                pass
        else:
            logger.debug(f"超时,未找到{image_path}")
            return False

    @classmethod
    def not_process(cls, image_path, timeout, confidence = 0.95, more_control_time = 0, more_control_sleep = 0):
        image = image_path
        start_time = time.time()
        logger.debug(f"开始查找{image_path},目标not_process,最高超时时间{timeout}秒")
        while time.time() - start_time <= timeout:
            try:
                location=pyautogui.center(pyautogui.locateOnScreen(Image.open(image), confidence = confidence))
                logger.debug(f"已找到[{image_path}]位置,执行【不操作】")
                return True
            except FileNotFoundError:
                logger.error(f"未找到{image_path}文件,请检查文件是否存在")
                return False
            except:
                pass
        else:
            logger.debug(f"超时,未找到{image_path}")
            return False
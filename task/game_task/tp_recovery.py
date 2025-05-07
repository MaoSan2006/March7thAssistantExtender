from venv import logger
import pyautogui
import time
import logging
from task.handler.auto_process_handler import auto_process_handler
logger = logging.getLogger("tp_recovery")

def tp_recovery():
    error_time = 0
    while error_time <= 30:
        #设置超时时间
        if error_time == 30:
            break
        #打开地图
        elif auto_process_handler.not_process("image/tp_recovery/tp_map1.png", 0.2, confidence = 0.9)==False and auto_process_handler.not_process("image/tp_recovery/tp_map2.png", 0.2, confidence = 0.9) == False:
            logger.info(f"打开地图")
            pyautogui.typewrite("m")
            time.sleep(1.5)
        #终末视界关闭
        elif auto_process_handler.click("image/tp_recovery/end_visit.png", 0.2, confidence = 0.9) == True:
            logger.info(f"关闭终末视界")
        #有可用锚点
        elif auto_process_handler.click("image/tp_recovery/tp_place.png", 0.2, confidence = 0.9) == True:
            logger.info(f"有可用锚点")
        #传送
        elif auto_process_handler.click("image/tp_recovery/tp.png", 0.2, confidence = 0.9) == True:
            logger.info(f"传送")
            return True
        #选择罗浮地图
        elif auto_process_handler.click("image/tp_recovery/luofu.png", 0.2, confidence = 0.9) == True:
            logger.info(f"选择罗浮地图")
            time.sleep(3)
        #选择长乐天
        elif auto_process_handler.click("image/tp_recovery/clt.png", 0.2, confidence = 0.9) == True:
            logger.info(f"选择长乐天")
            time.sleep(1)
        #打开星轨地图
        elif auto_process_handler.click("image/tp_recovery/star_map1.png", 0.2, confidence = 0.9) == True or auto_process_handler.click("image/tp_recovery/star_map2.png", 0.2, confidence = 0.9) == True:
            logger.info(f"打开星轨地图")
            time.sleep(3)
    return False
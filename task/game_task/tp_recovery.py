from venv import logger
import pyautogui
import time
import logging
from task.handler.auto_process_handler import auto_process_handler
from task.game_task.monthly_card import monthly_card
logger = logging.getLogger("tp_recovery")

def tp_recovery():
    error_time = 0
    while error_time <= 10:
        #月卡领取
        if auto_process_handler.not_process("image/pre_march7th/monthly_card.png", 0.5) == True:
            logger.info(f"月卡领取")
            monthly_card()
        #打开地图
        elif auto_process_handler.not_process("image/tp_recovery/tp_map1.png", 0.2, confidence = 0.9)==False and auto_process_handler.not_process("image/tp_recovery/tp_map2.png", 0.2, confidence = 0.9) == False:
            logger.info(f"打开地图")
            pyautogui.typewrite("m")
            time.sleep(1.5)
        #终末视界关闭
        elif auto_process_handler.click("image/tp_recovery/end_visit.png", 0.2, confidence = 0.9) == True:
            logger.info(f"关闭终末视界")
        #传送
        elif auto_process_handler.click("image/tp_recovery/tp.png", 0.2, confidence = 0.9) == True:
            logger.info(f"传送")
            return True
        #有可用锚点
        elif auto_process_handler.click("image/tp_recovery/taipusi_teleporter.png", 0.2, confidence = 0.9) == True:
            logger.info(f"有可用锚点")
        #选择罗浮地图
        elif auto_process_handler.click("image/tp_recovery/luofu.png", 0.2, confidence = 0.9) == True:
            logger.info(f"选择罗浮地图")
            time.sleep(3)
        #选择长乐天
        elif auto_process_handler.click("image/tp_recovery/taipusi.png", 0.2, confidence = 0.9) == True:
            logger.info(f"选择长乐天")
            time.sleep(1)
        #打开星轨地图
        elif auto_process_handler.click("image/tp_recovery/star_map1.png", 0.2, confidence = 0.9) == True or auto_process_handler.click("image/tp_recovery/star_map2.png", 0.2, confidence = 0.9) == True:
            logger.info(f"打开星轨地图")
            time.sleep(3)
    else:
        logger.error(f"传送超时")
        return False
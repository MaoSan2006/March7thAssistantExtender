from socket import timeout
from task.handler import process_handler
from task.handler.auto_process_handler import auto_process_handler
from task.handler.config_handler import config_handler
from task.handler.excel_handler import excel_handler
from task.handler.time_handler import nowtime
from task.handler.pre_march7th_handler import pre_march7th_handler
from task.handler.mid_march7th_handler import mid_march7th_handler
import os
import time
import logging

logger = logging.getLogger("switch_account_handler")

def one_account():
    logger.info("------------------------------开始单账号模式---------------------------------------")
    logger.info(f"++++++++++++++++++++分割线++++++++++++++++++++")
    logger.info(f"启动游戏中")
    os.startfile(config_handler("StarRail_path"))
    time.sleep(20)
    while error_time <= 60:
        if auto_process_handler.click("image/more_account_mode/enter.png", 0.2) == True:
            error_time = 0
            logger.info(f"进入游戏")
            break
        elif auto_process_handler.click("image/more_account_mode/game_in_start.png", 0.2) == True:
            error_time = 0
            logger.info(f"开始游戏")
        else:
            error_time += 1
    else:
        logger.error(f"进入游戏超时")
        return False
    while error_time <= 60:
        try:
            if pre_march7th_handler() == False:
                return False
            start_time = time.time()
            timeout = config_handler("timeout")
            while time.time() - start_time <= timeout:
                if process_handler.find_process("StarRail.exe") == False:
                    logger.info(f"完成任务")
                    process_handler.kill_process("March7th Assistant.exe")
                    process_handler.kill_process("PaddleOCR-json.exe")
                    return True
                elif auto_process_handler.click("image/more_account_mode/login_other_device.png", 1, confidence = 0.85) == True:
                    logger.info(f"当前账号在其他设备登录")
                    process_handler.kill_process("March7th Assistant.exe")
                    process_handler.kill_process("PaddleOCR-json.exe")
                    return False
            else:
                logger.info(f"运行超时")
                process_handler.kill_process("March7th Assistant.exe")
                process_handler.kill_process("PaddleOCR-json.exe")
        except Exception as e:
            logger.error(f"运行出错：{e}")
            process_handler.kill_process("March7th Assistant.exe")
            process_handler.kill_process("PaddleOCR-json.exe")
            process_handler.kill_process("StarRail.exe")
            return False
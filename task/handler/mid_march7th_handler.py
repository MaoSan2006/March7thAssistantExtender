
from task.handler.auto_process_handler import auto_process_handler 
from task.handler.end_marth7th_handler import end_march7th_handler
from task.handler.config_handler import config_handler
from task.handler.process_handler import process_handler
from task.handler.end_marth7th_handler import end_march7th_handler
import logging
import time

logger = logging.getLogger("mid_march7th_handler")

def mid_march7th_handler(id):
    timeout = config_handler("timeout")
    start_time = time.time()
    while time.time() - start_time <= timeout:
        if process_handler.find_process("StarRail.exe")==False:
            logging.info(f"完成任务")
            end_march7th_handler(id, "完成")
            break
        elif auto_process_handler.click("image/more_account_mode/login_other_device.png",1, confidence = 0.85) == True:
            logging.info(f"当前账号在其他设备登录")
            end_march7th_handler(id, "顶号")
            break
        else:
            time.sleep(10)
    else:
        logging.info(f"运行超时")
        end_march7th_handler(id, "超时")
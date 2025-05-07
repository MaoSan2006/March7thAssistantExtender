from task.handler.auto_process_handler import auto_process_handler
from task.handler.config_handler import config_handler
from task.game_task.monthly_card import monthly_card
from task.game_task.tp_recovery import tp_recovery
import logging

logger = logging.getLogger("pre_march7th_handler")

def pre_march7th_handler():
    error_time = 0
    while True:
        if error_time >= 60:
            logging.error(f"运行三月七助手前操作超时")
            return False
        elif auto_process_handler.not_process("image/pre_march7th/monthly_card.png", 0.5):
            logging.info(f"已订阅月卡，正在领取")
            monthly_card()
        elif auto_process_handler.not_process("image/pre_march7th/mobile.png", 0.5) or auto_process_handler.not_process("image/pre_march7th/mobile_red.png", 0.5):
            logging.info(f"已进入游戏页面")
            if config_handler("tp_recovery") == True:
                logging.info(f"开始锚点回血")
                tp_recovery()
            return True
        else:
            error_time += 1
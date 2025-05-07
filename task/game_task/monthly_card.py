from task.handler.auto_process_handler import auto_process_handler
import logging
logger = logging.getLogger("monthly_card")

def monthly_card():
    if auto_process_handler.click("image/month_card/monthly_card.png", 3.5, confidence = 0.8, more_control_time = 1, more_control_sleep = 5) == True:
        logger.info(f"识别到月卡领取界面")
    else:
        logger.error(f"月卡未订阅")
        return False
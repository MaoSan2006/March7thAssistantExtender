import os
import time
import logging
from task.handler.process_handler import process_handler
from task.handler.config_handler import config_handler
from task.handler.auto_process_handler import auto_process_handler

logger = logging.getLogger("game_auto_update")

def game_auto_update():
    logger.info("---------------------------------游戏自动更新------------------------------------------")
    try:
        #获取启动器路径并打开
        mhy_launcher_path = config_handler("mhy_launcher_path")
        if mhy_launcher_path == None:
            logger.error(f"米哈游启动器路径[{mhy_launcher_path}]未设置")
            return False
        os.startfile(mhy_launcher_path)
    except FileNotFoundError:
        logger.error(f"米哈游启动器路径[{mhy_launcher_path}]未设置或设置错误")
    except Exception as error_exception:
        logger.error(f"未知错误")
        logger.error(f"{error_exception}")
        return False
        #检测启动器页面是否显示
    if auto_process_handler.move("image/launcher/launcher_icro.png", 30)==False:
        return False
    #检测启动器有无更新
    if auto_process_handler.click("image/launcher/launcher_update.png", 3)==True or auto_process_handler.click("image/launcher/launcher_update1.png", 3)==True:
        if auto_process_handler.move("image/launcher/launcher_icro.png", 60)==True:
            logger.info("米哈游启动器更新")
        else:
            logger.error("米哈游启动器更新超时")
            return False
    else:
        logger.info("米哈游启动器已经是最新版本了")
    #切换游戏板块
    if auto_process_handler.click("image/launcher/game_icro.png", 3, confidence=0.75)==True:
        logger.info(f"已切换至崩铁板块")
    else:
        logger.error(f"无法切换至崩铁板块")
        return False
    #检测游戏更新
    error_time=0
    if auto_process_handler.click("image/game_auto_update/game_update.png", 5)==True:
        logger.info(f"检测到游戏有更新，开始更新")
        auto_process_handler.move("image/launcher/launcher_icro.png", 3)
        while error_time<=60:
            #启动器更新游戏
            if auto_process_handler.not_process("image/game_auto_update/game_out_download.png", 0.2)==True:
                error_time=0
                logger.info(f"下载中")
                while True:
                    if auto_process_handler.not_process("image/game_auto_update/game_out_download.png",0.2)==False:
                        break
            elif auto_process_handler.not_process("image/game_auto_update/check.png", 0.2)==True:
                error_time=0
                logger.info(f"校验中")
                while True:
                    if auto_process_handler.not_process("image/game_auto_update/check.png",0.2)==False:
                        break
            elif auto_process_handler.not_process("image/game_auto_update/extract.png", 0.2)==True:
                error_time=0
                logger.info(f"解压中")
                while True:
                    if auto_process_handler.not_process("image/game_auto_update/extract.png",0.2)==False:
                        break
            elif auto_process_handler.not_process("image/game_auto_update/over_check.png", 0.2)==True:
                error_time=0
                logger.info(f"完整性校验中")
                while True:
                    if auto_process_handler.not_process("image/game_auto_update/over_check.png",0.2)==False:
                        break
            elif auto_process_handler.not_process("image/game_auto_update/download_missfile.png", 0.2)==True:
                error_time=0
                logger.info(f"下载缺失资源中")
                while True:
                    if auto_process_handler.not_process("image/game_auto_update/download_missfile.png",0.2)==False:
                        break
            elif auto_process_handler.click("image/game_auto_update/game_start.png", 0.2)==True:
                error_time=0
                logger.info(f"游戏更新完成，开始游戏内更新")
                os.startfile(config_handler("StarRail_path"))
                time.sleep(20)
                break
            else:
                error_time+=1
        else:
            logger.error(f"启动器更新游戏超时")
            return False
        #关闭启动器
        process_handler.kill_process("HYP.exe")
        #游戏内更新
        while error_time<=60:
            if auto_process_handler.click("image/game_auto_update/confirm.png", 0.2)==True:
                error_time=0
                logger.info(f"同意用户协议")
            elif auto_process_handler.not_process("image/game_auto_update/check_data_update.png", 0.2)==True:
                error_time=0
                logger.info(f"正在检查数据更新")
                while True:
                    if auto_process_handler.not_process("image/game_auto_update/check_update.png",0.2)==False:
                        break
            elif auto_process_handler.not_process("image/game_auto_update/game_in_download.png", 0.2)==True:
                error_time=0
                logger.info(f"下载资源中")
                while True:
                    if auto_process_handler.not_process("image/game_auto_update/game_in_download.png",0.2)==False:
                        break
            elif auto_process_handler.not_process("image/game_auto_update/check_data.png", 0.2)==True:
                error_time=0
                logger.info(f"资源校验中")
                while True:
                    if auto_process_handler.not_process("image/game_auto_update/check_data.png",0.2)==False:
                        break
            elif auto_process_handler.not_process("image/game_auto_update/game_update_and_reboot.png", 0.2)==True:
                error_time=0
                logger.info("游戏更新完成，即将重启")         
                auto_process_handler.click("image/game_auto_update/yes.png", 0.2)
                time.sleep(20)
            else:
                error_time+=1
        else:
            logger.error(f"游戏内更新超时")
            return False
    else:
        logger.error(f"游戏已经是最新版本了,无需更新!")
        return False
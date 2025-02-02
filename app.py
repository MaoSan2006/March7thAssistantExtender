# -*- coding: utf-8 -*-
####################导入运行库和切换目录####################
import os
import yaml
import cv2
import pyautogui
import time
import logging
import subprocess
import requests
import sys
import pytesseract
import re
import pyuac
import pyscreeze
from PIL import Image, ImageFilter
os.chdir(os.path.dirname(sys.executable) if getattr(sys, 'frozen', False)else os.path.dirname(os.path.abspath(__file__)))
print(os.path.dirname(sys.executable) if getattr(sys, 'frozen', False)else os.path.dirname(os.path.abspath(__file__)))
####################当前时间####################
def nowtime():
    return time.strftime("%Y%m%d%H%M%S",time.localtime())
####################设置日志####################
log_file_path = os.path.join("log", nowtime() + ".log")
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(log_file_path)
    ]
)
logging.getLogger('PIL').setLevel(logging.WARNING)
####################读取config.yaml文件中的key参数####################
def get_config(key):
    try:
        with open('config.yaml','r',encoding='utf-8') as file:
            config=yaml.safe_load(file)
            return config.get(key)
    except FileNotFoundError:
        logging.error(f"未找到config.yaml文件,请检查是否存在或压缩包是否提取完整")
        return None
    except yaml.YAMLError as error_yaml:
        logging.error(f"YAML库错误")
        print(f"{error_yaml}")
        return None
    except KeyError as error_key:
        logging.error(f"config.yaml文件中未找到{key}参数")
        return None
    except Exception as error_exception:
        logging.error(f"未知错误")
        return None
####################仿真操作####################
def process(img_path,timeout,set_confidence,control,text):
    start_time=time.time()
    image=img_path
    logging.debug(f"开始查找{img_path}，目标{control}，最高超时时间{timeout}秒，最低置信度{set_confidence}")
    while True:
        try:
            location=pyautogui.center(pyautogui.locateOnScreen(image,confidence=set_confidence))
            if control=="click":
                pyautogui.click(location)
            elif control=="move":
                pyautogui.moveTo(location)
            logging.debug(f"已找到{img_path}位置并执行{control}")
            return True
        except:
            if time.time()-start_time>timeout:
                break
    logging.debug(f"未找到{img_path}")
    return False
####################主程序——自动更新游戏####################
def main_game_auto_update():
    logging.info("--------------------------------------游戏自动更新-----------------------------------------------")
    try:
        #获取启动器路径并打开
        mhy_launcher_path=get_config("mhy_launcher_path")
        if mhy_launcher_path==None:
            logging.error("米哈游启动器路径[mhy_launcher_path]未设置")
            return False
        os.startfile(mhy_launcher_path)
        #检测启动器页面是否显示
        if process("imgs/launcher_icro.png",10,0.7,"move","米哈游启动器图标")==False:
            return False
        if process("imgs/launcher_update.png",1,0.95,"click","米哈游启动器更新并重启")==True:
            if process("imgs/launcher_icro.png",60,0.95,"move","米哈游启动器图标")==True:
                logging.info("米哈游启动器更新")
            else:
                logging.error("米哈游启动器更新超时")
                return False
        #依次检测匹配
        error_time=0
        while_time=1
        flag=True
        while error_time<=10 and flag==True:
            logging.debug(f"当前错误次数为{error_time}")
            logging.debug(f"当前循环次数为{while_time}")
            if process("imgs/game_update.png",0.1,0.95,"click","崩铁更新游戏")==True:
                logging.info("检测到游戏有更新，开始更新.......")
                process("imgs/launcher_icro.png",10,0.95,"click","米哈游启动器图标")
            elif process("imgs/game_out_download.png",0.1,0.95,"","下载中")==True:
                logging.info("下载中......")
                time.sleep(1)
                while True:
                    if process("imgs/game_out_download.png",0.1,0.95,"","下载中！")==False:
                        break
            elif process("imgs/check.png",0.1,0.95,"","校验中")==True:
                logging.info("校验中.......")
                while True:
                    if process("imgs/check.png",0.1,0.95,"","校验中")==False:
                        break
            elif process("imgs/extract.png",0.1,0.95,"","解压中")==True:
                logging.info("解压中.......")
                while True:
                    if process("imgs/extract.png",0.1,0.95,"","解压中！")==False:
                        break
            elif process("imgs/over_check.png",0.1,0.95,"","完整性校验")==True:
                logging.info("完整性校验中.......")
                while True:
                    if process("imgs/over_check.png",0.1,0.95,"","完整性校验中!")==False:
                        break             
            elif process("imgs/download_missfile.png",0.1,0.95,"","下载缺失资源")==True:
                logging.info("下载缺失资源中.......")
                while True:
                    if process("imgs/download_missfile.png",0.1,0.95,"","下载缺失资源中!")==False:
                        break
            elif process("imgs/game_start.png",0.1,0.95,"click","启动游戏")==True:
                logging.info("游戏更新完成，开始启动游戏.......")
                time.sleep(20)
            elif process("imgs/game_in_download.png",0.1,0.95,"","游戏内更新")==True:
                logging.info("游戏内更新中.......")
                while True:
                    if process("imgs/game_in_download.png",0.1,0.95,"","游戏内更新中!")==False:
                        break
            elif process("imgs/game_update_and_reboot.png",0.1,0.95,"","重启游戏提示")==True:
                logging.info("更新完成，准备重启游戏")
                process("imgs/yes.png",0.1,0.95,"click","确认重启")
                time.sleep(20)
            elif process("imgs/enter.png",0.1,0.95,"","点击进入游戏")==True:
                logging.info("进入游戏")
                break
            else:
                error_time+=1
                time.sleep(1)
    except Exception as error_exception:
        logging.error("游戏自动更新出错")
        logging.error(error_exception)
    logging.info("--------------------------------------游戏自动更新完成-----------------------------------------------")
####################主程序####################
if __name__ == "__main__":
    #设置日志等级
    if get_config("log_level")=="DEBUG":
        logging.getLogger().setLevel(logging.DEBUG)
    elif get_config("log_level")=="INFO":
        logging.getLogger().setLevel(logging.INFO)
    else:
        logging.error("日志等级设置错误")
    #游戏自动更新部分
    if  get_config("game_update")==True:
        logging.info("游戏自动更新设置为开启")
        main_game_auto_update()
    elif get_config("game_update")==False:
        logging.info("游戏自动更新设置为关闭")
    else:
        logging.error("游戏自动更新设置错误")
    #运行三月七助手部分
    if get_config("game_update_run_march7thAssistant")==True:
        match7thAssistant_path=get_config("March7thAssistant_path")
        if match7thAssistant_path==None:
            logging.error("三月七助手路径未设置")
        elif "March7th Assistant.exe" not in match7thAssistant_path:
            logging.error("三月七助手路径设置错误,需要包含'March7th Assistant.exe'")
        os.startfile(match7thAssistant_path)
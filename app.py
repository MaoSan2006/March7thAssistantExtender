# -*- coding: utf-8 -*-
print("+----------------------------------------------------------------------------------------------------------------------+")
print("|                                       欢迎使用 March7th Assistant Extender                                           |")
print("|                          March7thAssistant链接：https://github.com/moesnow/March7thAssistant                         |")
print("|                March7thAssistantExtender链接：https://github.com/MaoSan2006/March7thAssistantExtender                |")
print("|                                     此程序遵循GPL3.0开源协议，转载请注明出处！                                       |")
print("+----------------------------------------------------------------------------------------------------------------------+")
print("正在加载运行库，请稍后......")
#导入运行库和切换目录
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
import pandas
import openpyxl
import psutil
import shutil
from PIL import Image, ImageFilter
os.chdir(os.path.dirname(sys.executable) if getattr(sys, 'frozen', False)else os.path.dirname(os.path.abspath(__file__)))
print("运行库加载完成")
#当前时间
def nowtime():
    return time.strftime("%Y%m%d",time.localtime())
#设置日志格式
log_file_path = os.path.join("log", nowtime() + ".log")
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(log_file_path)
    ]
)
logging.getLogger('PIL').setLevel(logging.WARNING)    
#读取config.yaml文件中的key参数
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
#标记每个账号状态
def mark_over_account(id,state):
    file=pandas.read_excel('account.xlsx')
    file.at[id,nowtime()]=state
    file.to_excel('account.xlsx',index=False)
    return file
#检查今天日期存入
def check_date(file):
    if nowtime() not in file.columns:
        logging.info('检测到今日首次运行')
        logging.info(f'正在写入今日日期({nowtime()})到account.xlsx文件中')
        file.insert(len(file.columns),nowtime(),"")
        file.to_excel('account.xlsx', index=False)
        return file
    return file
#查找进程(通过进程名)
def find_process(process_name):
    for proc in psutil.process_iter():
        try:
            if process_name.lower() in proc.name().lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False
#结束进程(通过进程名)
def kill_process(process_name):
    try:
        subprocess.Popen(["taskkill", "/f", "/im", process_name])
        logging.debug(f"已结束进程{process_name}")
        return True
    except:
        logging.error(f"结束进程{process_name}失败")
        return False
#仿真操作
def process(image_path,timeout,control,confidence=0.95,more_control_time=0,more_control_sleep=0):
    start_time=time.time()
    image=image_path
    logging.debug(f"开始查找{image_path}，目标{control}，最高超时时间{timeout}秒")
    while True:
        try:
            location=pyautogui.center(pyautogui.locateOnScreen(Image.open(image),confidence=confidence))
            if control=='click':
                pyautogui.click(location)
                while more_control_time>0:
                    time.sleep(more_control_sleep)
                    more_control_time-=1
                    pyautogui.click(location)
            elif control=='move':
                pyautogui.moveTo(location)
                while more_control_time>0:
                    time.sleep(more_control_sleep)
                    more_control_time-=1
                    pyautogui.moveTo(location)
            logging.debug(f"已找到{image_path}位置并执行{control}")
            return True
        except FileNotFoundError:
            logging.error(f"未找到{image_path}文件")
            return False
        except:
            if time.time()-start_time>timeout:
                break
    logging.debug(f"未找到{image_path}")
    return False
#月卡领取
def month_card():
    if process("image/month_card/monthly_card.png",10,"click",confidence=0.8,more_control_time=1,more_control_sleep=5)==True:
        logging.info(f"识别到月卡领取界面")
    else:
        logging.error(f"月卡未订阅")
        return False
#锚点回血
def tp_recovery():
    error_time=0
    while error_time<=30:
        #设置超时时间
        if error_time==30:
            break
        #打开地图
        elif process("image/tp_recovery/tp_map1.png",0.2,"click",confidence=0.9)==False and process("image/tp_recovery/tp_map2.png",0.2,"click",confidence=0.9)==False:
            logging.info(f"打开地图")
            pyautogui.typewrite("m")
        #终末视界关闭
        elif process("image/tp_recovery/end_visit.png",0.2,"click",confidence=0.9)==True:
            logging.info(f"关闭终末视界")
        #有可用锚点
        elif process("image/tp_recovery/tp_place.png",0.2,"click",confidence=0.9)==True:
            logging.info(f"有可用锚点")
        #传送
        elif process("image/tp_recovery/tp.png",0.2,"click",confidence=0.9)==True:
            logging.info(f"传送")
            return True
        #打开星轨地图
        elif process("image/tp_recovery/star_map1.png",0.2,"click",confidence=0.9)==True or process("image/tp_recovery/star_map2.png",0.2,"click",confidence=0.9)==True:
            logging.info(f"打开星轨地图")
        #选择长乐天
        elif process("image/tp_recovery/clt.png",0.2,"click",confidence=0.9)==True:
            logging.info(f"选择长乐天")
    return False
#运行三月七助手前操作
def pre_march7th():
    error_time=0
    while True:
        if error_time>=60:
            logging.error(f"运行三月七助手前操作超时")
            return False
        elif process("image/pre_march7th/month_card_title.png",0.5,""):
            logging.info(f"已订阅月卡，正在领取")
            month_card()
        elif process("image/pre_march7th/mobile.png",0.5,"") or process("image/pre_march7th/mobile_red.png",0.5,""):
            logging.info(f"已进入游戏页面")
            if get_config("tp_recovery")==True:
                logging.info(f"开始锚点回血")
                tp_recovery()
            return True
        else:
            error_time+=1
#自动更新游戏
def main_game_auto_update():
    logging.info("---------------------------------游戏自动更新------------------------------------------")
    try:
        #获取启动器路径并打开
        mhy_launcher_path=get_config("mhy_launcher_path")
        if mhy_launcher_path==None:
            logging.error(f"米哈游启动器路径[{mhy_launcher_path}]未设置")
            return False
        os.startfile(str(mhy_launcher_path)+"launcher.exe")
    except FileNotFoundError:
        logging.error(f"米哈游启动器路径[{mhy_launcher_path}]未设置或设置错误")
    except Exception as error_exception:
        logging.error(f"未知错误")
        logging.error(f"{error_exception}")
        return False
        #检测启动器页面是否显示
    if process("image/launcher/launcher_icro.png",30,"move")==False:
        return False
    #检测启动器有无更新
    if process("image/launcher/launcher_update.png",3,"click")==True or process("image/launcher/launcher_update1.png",3,"click")==True:
        if process("image/launcher/launcher_icro.png",60,"move")==True:
            logging.info("米哈游启动器更新")
        else:
            logging.error("米哈游启动器更新超时")
            return False
    else:
        logging.info("米哈游启动器已经是最新版本了")
    #开始检测更新
    if process("image/launcher/game_icro.png",3,"click")==True:
        logging.info(f"切换至崩铁板块")
    else:
        logging.error(f"无法切换至崩铁板块")
        return False
    #检测游戏更新
    error_time=0
    if process("image/game_auto_update/game_update.png",5,"click")==True:
        logging.info(f"检测到游戏有更新，开始更新")
        process("image/launcher/launcher_icro.png",30,"move")
        while error_time<=60:
            #游戏外更新
            if process("image/game_auto_update/game_out_download.png",0.2,"")==True:
                error_time=0
                logging.info(f"下载中")
                while True:
                    if process("image/game_auto_update/game_out_download.png",0.2,"")==False:
                        break
            elif process("image/game_auto_update/check.png",0.2,"")==True:
                error_time=0
                logging.info(f"校验中")
                while True:
                    if process("image/game_auto_update/check.png",0.2,"")==False:
                        break
            elif process("image/game_auto_update/extract.png",0.2,"")==True:
                error_time=0
                logging.info(f"解压中")
                while True:
                    if process("image/game_auto_update/extract.png",0.2,"")==False:
                        break
            elif process("image/game_auto_update/over_check.png",0.2,"")==True:
                error_time=0
                logging.info(f"完整性校验中")
                while True:
                    if process("image/game_auto_update/over_check.png",0.2,"")==False:
                        break
            elif process("image/game_auto_update/download_missfile.png",0.2,"")==True:
                error_time=0
                logging.info(f"下载缺失资源中")
                while True:
                    if process("image/game_auto_update/download_missfile.png",0.2,"")==False:
                        break
            elif process("image/game_auto_update/game_start.png",0.2,"click")==True:
                error_time=0
                logging.info(f"游戏更新完成，开始游戏内更新")
                break
            #游戏内更新
            elif process("image/game_auto_update/check_data_update.png",0.2,"")==True:
                error_time=0
                logging.info(f"正在检查数据更新")
                while True:
                    if process("image/game_auto_update/check_update.png",0.2,"")==False:
                        break
            elif process("image/game_auto_update/game_in_download.png",0.2,"")==True:
                error_time=0
                logging.info(f"下载资源中")
                while True:
                    if process("image/game_auto_update/game_in_download.png",0.2,"")==False:
                        break
            elif process("image/game_auto_update/check_data.png",0.2,"")==True:
                error_time=0
                logging.info(f"资源校验中")
                while True:
                    if process("image/game_auto_update/check_data.png",0.2,"")==False:
                        break
            elif process("image/game_auto_update/game_update_and_reboot.png",0.2,"")==True:
                error_time=0
                logging.info("游戏更新完成，即将重启")         
                process("image/game_auto_update/yes.png",0.2,"click")
                time.sleep(20)
            else:
                error_time+=1
        error_time=0
    else:
        logging.error(f"游戏已经是最新版本了,无需更新!")
        return False
#多账户模式
def main_switch_account():
    logging.info("------------------------------开始多账号模式---------------------------------------")
    file=pandas.read_excel("account.xlsx")
    file=check_date(file)
    for id in range(len(file)):
        error_time=0
        logging.info(f"已经完成{id}个账号")
        logging.info(f"当前账号为第{id+1}个账号")
        #获取账号和密码
        account=str(file.at[id,"账号"])
        password=str(file.at[id,"密码"])
        logging.info(f"账号{account}")
        logging.info(f"密码{password}")
        #启动游戏
        os.startfile(str(get_config("StarRail_path"))+"StarRail.exe")
        time.sleep(20)
        #退出账号与转到登录页面
        while error_time<=60:
            if process("image/more_account_mode/logout.png",0.5,"click")==True:
                error_time=0
                logging.info(f"退出当前账号")
                if process("image/more_account_mode/logout_confirm.png",3,"click")==True:
                    logging.info(f"确认退出账号")
                else:
                    logging.error(f"确认退出账号超时")
                    return False
            elif process("image/more_account_mode/login_other_account.png",0.5,"click")==True:
                error_time=0
                logging.info(f"登录其他账号")
            elif process("image/more_account_mode/account_password.png",0.5,"click")==True:
                error_time=0
                logging.info(f"使用账号密码登录")
                break
            else:
                error_time+=1
        else:
            logging.error(f"退出账号与转到登录页面超时")
            return False
        error_time=0
        #输入账号和密码
        while error_time<=60:
            if process("image/more_account_mode/account.png",0.5,"click")==True:
                error_time=0
                logging.info(f"输入账号中")
                pyautogui.write(account,0.35)
            elif process("image/more_account_mode/password.png",0.5,"click")==True:
                error_time=0
                logging.info(f"输入密码中")
                pyautogui.write(password,0.35)
                break
        #登录和账号密码错误检测
        error_time=0
        flag=True
        while error_time<=30 and flag==True:
            if process("image/more_account_mode/login.png",0.2,"click")==True:
                error_time=0
                logging.info(f"登录")
                process("image/more_account_mode/confirm.png",0.2,"click")
                logging.info(f"同意协议")
            elif process("image/more_account_mode/login_error.png",0.2,"click")==True:
                error_time=0
                logging.info(f"账号或密码错误")
                mark_over_account(id,"账号或密码错误")
                flag=False
            elif process("image/more_account_mode/enter.png",0.2,"click")==True:
                error_time=0
                logging.info(f"进入游戏")
                mark_over_account(id,"登录成功")
                break
            elif process("image/more_account_mode/game_in_start.png",0.2,"click")==True:
                error_time=0
                logging.info(f"开始游戏")
            else:
                error_time+=1
        time.sleep(10)
        pre_march7th()
        #切换用户设置
        logging.info(f"切换用户设置")
        user_config_path=os.path.join(os.getcwd(),"user_config",f"{account}.yaml")
        new=os.path.join(get_config("March7thAssistant_path"), "config.yaml")
        logging.debug(f"准备复制{account}.yaml到三月七助手目录")
        shutil.copy(user_config_path,new)
        logging.debug(f"完成")
        #开始运行三月七助手
        start_time=time.time()
        timeout=int(get_config("timeout"))
        os.startfile(str(get_config("March7thAssistant_path"))+"March7th Assistant.exe")
        while time.time()-start_time<=timeout:
            if find_process("StarRail.exe")==False:
                kill_process("March7th Assistant.exe")
                kill_process("PaddleOCR-json.exe")
                file=mark_over_account(id,"完成")
                break
            elif process("image/more_account_mode/login.other_device.png",1,"")==True:
                logging.info(f"当前账号在其他设备登录")
                kill_process("StarRail.exe")
                kill_process("March7th Assistant.exe")
                kill_process("PaddleOCR-json.exe")
                file=mark_over_account(id,"顶号")
                break
            else:
                time.sleep(10)
        else:
            kill_process("StarRail.exe")
            kill_process("March7th Assistant.exe")
            kill_process("PaddleOCR-json.exe")
            file=mark_over_account(id,"超时")
            break
    logging.info(f"------------------------------------------------")
#主程序
if __name__ == "__main__":
    #设置日志等级
    if get_config("log_level")=="DEBUG":
        logging.getLogger().setLevel(logging.DEBUG)
    elif get_config("log_level")=="INFO":
        logging.getLogger().setLevel(logging.INFO)
    else:
        logging.error("日志等级设置错误")
    #游戏自动更新部分
    if  get_config("game_auto_update")==True:
        logging.info("游戏自动更新设置为开启")
        main_game_auto_update()
    elif get_config("game_auto_update")==False:
        logging.info("游戏自动更新设置为关闭")
    else:
        logging.error("游戏自动更新设置错误")
    #单号运行或多号运行
    if get_config("mode_account_mode")==True:
        logging.info("账号运行类别：多账号模式")
        main_switch_account()
    elif get_config("mode_account_mode")==False:
        logging.info("账号运行类别：单账号模式")
        logging.info("单账号模式暂时不可用")
    else:
        logging.error("账号运行类别错误")
    #完成后操作
    if get_config("over_control")=="poweroff":
        logging.info("60秒后关机")
        time.sleep(60)
        os.system("shutdown -s -t 0")
    elif get_config("over_control")=="":
        sys.exit(0)
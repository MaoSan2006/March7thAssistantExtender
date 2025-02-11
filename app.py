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
import pandas
import openpyxl
import psutil
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
    format='%(asctime)s | %(levelname)s | %(message)s',
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
####################关键配置设置检测####################
def core_config_check():
    if get_config("log_level")==None:
        logging.error("未设置日志等级")
        return False
    elif get_config("log_level") not in ["DEBUG","INFO"]:
        logging.error("日志等级设置错误")
        return False
    elif get_config("March7thAssistant_path")==None:
        logging.error("未设置三月七助手路径")
        return False
    elif "March7th Assistant.exe" not in get_config("March7thAssistant_path"):
        logging.error("三月七助手路径设置错误，路径中需包含'March7th Assistant.exe'")
        return False
    if get_config("multi_account")==None:
        logging.error("未设置单账号/多账号模式")
        return False
    elif get_config("multi_account") not in [True,False]:
        logging.error("单账号/多账号模式设置错误")
        return False
    if get_config("multi_account")==True:
        if get_config("starrail_path")==None:
            logging.error("未设置崩铁游戏路径")
            return False
        elif "StarRail.exe" not in get_config("starrail_path"):
            logging.error("崩铁游戏路径设置错误，路径中需包含'StarRail.exe'")
            return False
    return True
####################标记每个账号状态####################
def mark_over_account(id,state,today_date):
    file=pandas.read_excel('account.xlsx')
    file[id,today_date]=state
    file.to_excel('account.xlsx',index=False)
    return file
####################检查今天日期存入####################
def check_date(today_date):
    file = pandas.read_excel('account.xlsx')
    if today_date not in file.columns:
        logging.info('今日首次运行')
        logging.info(f'正在写入今日日期({today_date})到account.xlsx文件中')
        file[today_date] = ''  # 直接创建列
        file.to_excel('account.xlsx', index=False)  # 保存文件
        return False
    return True
####################查找进程(通过进程名)####################
def find_process(process_name):
    for proc in psutil.process_iter():
        try:
            if process_name.lower() in proc.name().lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False
####################结束进程(通过进程名)####################
def kill_process(process_name):
    try:
        subprocess.Popen(["taskkill", "/f", "/im", process_name])
        logging.debug(f"已结束进程{process_name}")
        return True
    except:
        logging.error(f"结束进程{process_name}失败")
        return False
####################仿真操作####################
def process(img_path,timeout,set_confidence,control,text):
    start_time=time.time()
    image=img_path
    logging.debug(f"开始查找{img_path}，目标{control}，最高超时时间{timeout}秒，最低置信度{set_confidence}")
    while True:
        try:
            location=pyautogui.center(pyautogui.locateOnScreen(Image.open(image),confidence=set_confidence))
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
        if process("imgs/launcher_icro.png",30,0.7,"move","米哈游启动器图标")==False:
            return False
        if process("imgs/launcher_update.png",3,0.95,"click","米哈游启动器更新并重启")==True or process("imgs/launcher_update1.png",3,0.95,"click","米哈游启动器更新"):
            if process("imgs/launcher_icro.png",60,0.95,"move","米哈游启动器图标")==True:
                logging.info("米哈游启动器更新")
            else:
                logging.error("米哈游启动器更新超时")
                return False
        #依次检测匹配
        error_time=0
        while_time=1
        flag=True
        while error_time<=30 and flag==True:
            logging.debug(f"当前错误次数为{error_time}")
            logging.debug(f"当前循环次数为{while_time}")
            if process("imgs/game_update.png",0.1,0.95,"click","崩铁更新游戏")==True:
                error_time=0
                logging.info("检测到游戏有更新，开始更新.......")
                process("imgs/launcher_icro.png",10,0.95,"click","米哈游启动器图标")
            elif process("imgs/game_out_download.png",0.1,0.95,"","下载中")==True:
                error_time=0
                logging.info("下载中......")
                time.sleep(1)
                while True:
                    if process("imgs/game_out_download.png",0.1,0.95,"","下载中！")==False:
                        break
            elif process("imgs/check.png",0.1,0.95,"","校验中")==True:
                error_time=0
                logging.info("校验中.......")
                while True:
                    if process("imgs/check.png",0.1,0.95,"","校验中")==False:
                        break
            elif process("imgs/extract.png",0.1,0.95,"","解压中")==True:
                error_time=0
                logging.info("解压中.......")
                while True:
                    if process("imgs/extract.png",0.1,0.95,"","解压中！")==False:
                        break
            elif process("imgs/over_check.png",0.1,0.95,"","完整性校验")==True:
                error_time=0
                logging.info("完整性校验中.......")
                while True:
                    if process("imgs/over_check.png",0.1,0.95,"","完整性校验中!")==False:
                        break             
            elif process("imgs/download_missfile.png",0.1,0.95,"","下载缺失资源")==True:
                error_time=0
                logging.info("下载缺失资源中.......")
                while True:
                    if process("imgs/download_missfile.png",0.1,0.95,"","下载缺失资源中!")==False:
                        break
            elif process("imgs/game_start.png",0.1,0.95,"click","启动游戏")==True:
                error_time=0
                logging.info("游戏更新完成，开始启动游戏.......")
                time.sleep(20)
            elif process("imgs/game_in_download.png",0.1,0.95,"","游戏内更新")==True:
                error_time=0
                logging.info("游戏内更新中.......")
                while True:
                    if process("imgs/game_in_download.png",0.1,0.95,"","游戏内更新中!")==False:
                        break
            elif process("imgs/game_update_and_reboot.png",0.1,0.95,"","重启游戏提示")==True:
                error_time=0
                logging.info("更新完成，准备重启游戏")
                process("imgs/yes.png",0.1,0.95,"click","确认重启")
                time.sleep(20)
            elif process("imgs/enter.png",0.1,0.95,"","点击进入游戏")==True:
                error_time=0
                logging.info("进入游戏")
                break
            else:
                error_time+=1
                time.sleep(1)
    except Exception as error_exception:
        logging.error("游戏自动更新出错")
        logging.error(error_exception)
    logging.info("正在关闭游戏")
    kill_process("StarRail.exe")
    logging.info("--------------------------------------游戏自动更新完成-----------------------------------------------")
####################多号协同####################
def main_switch_account():
        logging.info("--------------------------------------开始多号协同-----------------------------------------------")
        file=pandas.read_excel("account.xlsx")
        if check_date(nowtime()[0:8])==True:
            logging.info("今天不是第一次运行了")
        else:
            logging.info("今天是第一次运行")
        for i in range(len(file)):
            logging.info(f"已经完成{i}个账号")
            logging.info(f"当前账号为第{i+1}个账号")
            #获取账号和密码
            account=file.loc[i,"账号"]
            password=file.loc[i,"密码"]
            logging.info(f"账号为{account}")
            logging.info(f"密码为{password}")
            #启动游戏
            os.startfile(get_config("starrail_path"))
            time.sleep(15)
            #初始化flag
            flag1=False
            flag2=False
            flag3=False
            #切号部分——退出账号
            if flag1==False:
                if process("imgs/logout.png",10,0.95,"click","退出账号")==True:
                    logging.info("退出账号")
                    if process("imgs/logout_confirm.png",10,0.95,"click","确认退出")==True:
                        logging.info("确认退出")
                        flag1=True
            #切号部分——切换登录模式
            if flag2==False:
                if process("imgs/login_other_account.png",10,0.95,"click","登录其他账号")==True:
                    logging.info("登录其他账号")
                    if process("imgs/account_passoword_login.png",10,0.95,"click","使用账号密码登录")==True:
                        logging.info("使用账号密码登录")
                        flag2=True
            #切号部分——登录账号
            if flag3==False:
                if process("imgs/account.png",10,0.95,"click","登录_输入账号")==True:
                    logging.info("登录_输入账号")
                    pyautogui.write(str(account),0.05)
                    if process("imgs/password.png",10,0.95,"click","登录_输入密码")==True:
                        logging.info("登录_输入密码")
                        pyautogui.write(str(password),0.05) 
                        if process("imgs/login.png",10,0.95,"click","登录")==True:
                            logging.info("进入游戏")
                            if process("imgs/confirm.png",10,0.95,"click","同意协议")==True:
                                logging.info("同意协议")
                                if process("imgs/account_error.png",10,0.95,"","账号或密码错误")==True:
                                    logging.info("账号或密码错误")
                                    file=mark_over_account(i,"账号或密码错误",nowtime()[0:8])
                                    continue
                                else:
                                    logging.info("登录成功")
                                    file=mark_over_account(i,"登录成功",nowtime()[0:8])
                                    flag3=True
            if flag1==True and flag2==True and flag3==True:
                flag1=False
                flag2=False
                flag3=False
                March7thAssistant_path=get_config("March7thAssistant_path")
                os.startfile(March7thAssistant_path)
                while True:
                    if find_process("StarRail.exe")==False:
                        kill_process("March7th Assistant.exe")
                        kill_process("PaddleOCR-json.exe")
                        break
                    time.sleep(1)                                     
            logging.info("--------------------------------------多号协同分割线-----------------------------------------------")
            time.sleep(15)
        logging.info("--------------------------------------结束多号协同-----------------------------------------------")
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
    #检测关键配置是否设置并正确
    if core_config_check()==True:
        logging.info("关键配置设置正确")
    else:
        os.system("pause")
    #单号运行或多号运行
    if get_config("multi_account")==True:
        logging.info("多号协同设置为开启")
        main_switch_account()
    elif get_config("multi_account")==False:
        logging.info("多号协同设置为关闭")
    else:
        logging.error("多号协同设置错误")
    #完成后操作
    if get_config("over_control")=="poweroff":
        logging.info("60秒后关机")
        time.sleep(60)
        os.system("shutdown -s -t 0")
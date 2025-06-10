from task.handler.auto_process_handler import auto_process_handler
from task.handler.config_handler import config_handler
from task.handler.excel_handler import excel_handler
from task.handler.time_handler import nowtime
from task.handler.mid_march7th_handler import mid_march7th_handler
from task.handler.pre_march7th_handler import pre_march7th_handler
from task.handler.excel_handler import excel_handler
from task.handler.process_handler import process_handler
import pandas
import pyautogui
import os
import time
import logging
import shutil
import pyperclip
import win32gui
import win32con

logger = logging.getLogger("switch_account_handler")

def switch_account():
    logger.info("------------------------------开始多账号模式---------------------------------------")
    if excel_handler.find_column(nowtime()) == False:
        excel_handler.write_excel_column(nowtime())
    file=pandas.read_excel('account.xlsx')
    for id in range(len(file)):
        logger.info(f"++++++++++++++++++++分割线++++++++++++++++++++")
        error_time=0
        logger.info(f"已经完成{id}个账号")
        logger.info(f"当前账号为第{id+1}个账号")
        #获取账号和密码
        account=str(file.at[id,"账号"])
        password=str(file.at[id,"密码"])
        logger.info(f"账号{account}")
        logger.info(f"密码{password[0:3]}***{password[-3:]}")
        if pandas.notna(file.at[id, nowtime()]):
            logger.info(f"该账户今日已经运行过了，跳过")
            continue
        #启动游戏
        if process_handler.find_process("StarRail.exe") == True:
            logger.debug("游戏已经运行，跳过")
        else:
            logger.info(f"启动游戏中......")
            os.startfile(config_handler.read("StarRail_path"))
            hwnd = win32gui.FindWindow(None, "崩坏：星穹铁道")
            if hwnd != 0:
                # 使窗口显示在最前面
                win32gui.ShowWindow(hwnd, win32con.SW_SHOWNORMAL)
                win32gui.SetForegroundWindow(hwnd)
            else:
                logger.warning("未找到 StarRail.exe 窗口")
        time.sleep(20)
        #退出账号与转到登录页面
        while error_time<=60:
            if auto_process_handler.click("image/more_account_mode/logout.png", 0.5) == True:
                error_time=0
                logger.info(f"退出当前账号")
                if auto_process_handler.click("image/more_account_mode/logout_confirm.png", 3) == True:
                    logger.info(f"确认退出账号")
                else:
                    logger.error(f"确认退出账号超时")
                    return False
            elif auto_process_handler.click("image/more_account_mode/login_other_account.png", 0.5) == True:
                error_time=0
                logger.info(f"登录其他账号")
            elif auto_process_handler.click("image/more_account_mode/account_password.png", 0.5) == True:
                error_time=0
                logger.info(f"使用账号密码登录")
                break
            else:
                error_time+=1
        else:
            logger.error(f"退出账号与转到登录页面超时")
            return False
        error_time=0
        #输入账号和密码
        while error_time<=60:
            if auto_process_handler.click("image/more_account_mode/account.png", 0.5) == True:
                error_time=0
                logger.info(f"输入账号中")
                pyperclip.copy(account)
                pyautogui.hotkey('ctrl', 'v')
                time.sleep(1)
                auto_process_handler.click("image/more_account_mode/password.png", 0.5)
                logger.info(f"输入密码中")
                pyperclip.copy(password)
                pyautogui.hotkey('ctrl', 'v')
                break
        #登录和账号密码错误检测
        error_time=0
        flag=True
        while error_time<=30 and flag==True:
            if auto_process_handler.click("image/more_account_mode/login.png", 0.2) == True:
                error_time=0
                logger.info(f"登录")
                auto_process_handler.click("image/more_account_mode/confirm.png", 0.2)
                logger.info(f"同意协议")
            elif auto_process_handler.click("image/more_account_mode/login_error.png", 0.2) == True:
                error_time=0
                logger.info(f"账号或密码错误")
                excel_handler.write_excel(id, nowtime(), "账号或密码错误")
                flag=False
            elif auto_process_handler.click("image/more_account_mode/enter.png", 0.2) == True:
                error_time=0
                logger.info(f"进入游戏")
                excel_handler.write_excel(id, nowtime(), "登录成功")
                break
            elif auto_process_handler.click("image/more_account_mode/game_in_start.png", 0.2) == True:
                error_time=0
                logger.info(f"开始游戏")
            else:
                error_time+=1
        time.sleep(10)
        pre_march7th_handler()
        #切换用户设置
        logger.info(f"切换用户设置")
        user_config_path = os.path.join(os.getcwd(), "user_config", f"{account}.yaml")
        new = os.path.join(os.path.dirname(config_handler.read("March7thAssistant_path")), "config.yaml")
        logger.debug(f"准备复制{account}.yaml到三月七助手目录")
        shutil.copy(user_config_path,new)
        logger.debug(f"复制完成，正在拉起三月七助手")
        os.startfile(config_handler.read("March7thAssistant_path"))
        #开始运行三月七助手
        mid_march7th_handler(id)
    logger.info(f"------------------------------------------------")
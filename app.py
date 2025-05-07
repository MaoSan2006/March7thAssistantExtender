# -*- coding: utf-8 -*-
print("+----------------------------------------------------------------------------------------------------------------------+")
print("|                                                版本V2025.05.07                                                       |")
print("|                                       欢迎使用 March7th Assistant Extender                                           |")
print("|                          March7thAssistant链接：https://github.com/moesnow/March7thAssistant                         |")
print("|                March7thAssistantExtender链接：https://github.com/MaoSan2006/March7thAssistantExtender                |")
print("|                                     此程序遵循GPL3.0开源协议，转载请注明出处！                                       |")
print("+----------------------------------------------------------------------------------------------------------------------+")
print("正在加载运行库，请稍后......")
#导入第三方运行库和切换目录
import os
import logging
import sys
import time
#导入自定义运行库
from task.handler.config_handler import config_handler
from task.handler.time_handler import nowtime
#切换目录
os.chdir(os.path.dirname(sys.executable) if getattr(sys, 'frozen', False)else os.path.dirname(os.path.abspath(__file__)))
print("运行库加载完成")

#设置日志格式
log_file_path = os.path.join("log", nowtime()+ ".log")
logging.basicConfig(
    level=logging.INFO if config_handler("log_level") == "DEBUG" else logging.DEBUG,
    format='%(asctime)s | %(levelname)s | %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(log_file_path)
    ]
)
logging.getLogger('PIL').setLevel(logging.WARNING)

if __name__ == "__main__":
    #更新检查
    from task.handler.check_update_handler import check_update
    if config_handler("check_update") == True:
        check_update.check_update()
    elif config_handler("check_update") == False:
        logging.info("更新检查已关闭")
    else:
        logging.error("配置文件错误：更新检查")
        sys.exit()
    #画质设置
    import winreg
    from task.handler.reg_handler import reg_handler
    originally_quality = {
        "width" : reg_handler.read_reg_jsondata(winreg.HKEY_CURRENT_USER, r"Software\miHoYo\崩坏：星穹铁道", "GraphicsSettings_PCResolution_h431323223", "width"),
        "height" : reg_handler.read_reg_jsondata(winreg.HKEY_CURRENT_USER, r"Software\miHoYo\崩坏：星穹铁道", "GraphicsSettings_PCResolution_h431323223", "height"),
        "isFullScreen" : reg_handler.read_reg_jsondata(winreg.HKEY_CURRENT_USER, r"Software\miHoYo\崩坏：星穹铁道", "GraphicsSettings_PCResolution_h431323223", "isFullScreen"),
        "HDR": reg_handler.read_reg_data(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\DirectX\UserGpuPreferences", config_handler("StarRail_path")),
        "flag" : False 
    }
    logging.info(f"当前分辨率:{originally_quality['width']}x{originally_quality['height']}")
    logging.info(f"全屏模式:{"开" if {originally_quality['isFullScreen']} == True else "关"}")
    logging.info(f"HDR模式:{'开' if originally_quality['HDR'] == 'AutoHDREnable=2097;' else '关' if originally_quality['HDR'] == 'AutoHDREnable=2096;' else '关'}")
    if originally_quality["width"] != 1920 or originally_quality["height"] != 1080 or originally_quality["isFullScreen"] != False or originally_quality["HDR"] == "AutoHDREnable=2097;":
        originally_quality["flag"] = True
        logging.info("当前画质设置与预设不同，正在设置为预设")
        logging.info("运行完成后会自动恢复")
        reg_handler.write_reg_jsondata(winreg.HKEY_CURRENT_USER, r"Software\miHoYo\崩坏：星穹铁道", "GraphicsSettings_PCResolution_h431323223", "width", 1920)
        reg_handler.write_reg_jsondata(winreg.HKEY_CURRENT_USER, r"Software\miHoYo\崩坏：星穹铁道", "GraphicsSettings_PCResolution_h431323223", "height", 1080)
        reg_handler.write_reg_jsondata(winreg.HKEY_CURRENT_USER, r"Software\miHoYo\崩坏：星穹铁道", "GraphicsSettings_PCResolution_h431323223", "isFullScreen", False)
        reg_handler.write_reg_data(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\DirectX\UserGpuPreferences", os.path.normcase(config_handler("StarRail_path")), "AutoHDREnable=2096;")
    #游戏更新检查
    if config_handler("game_auto_update") == True:
        logging.info("游戏更新检查已开启")
        from task.game_task.game_auto_update import game_auto_update
        game_auto_update()
    elif config_handler("game_auto_update") == False:
        logging.info("游戏更新检查已关闭")
    else:
        logging.error("配置文件错误：游戏更新检查")
        sys.exit()
    #运行账号类别
    if config_handler("account_mode") == True:
        logging.info("运行账号类别：多账号")
        from task.game_task.switch_account import switch_account
        switch_account()
    elif config_handler("account_mode") == False:
        logging.info("运行账号类别：单账号")
        logging.warning("需要提前登录账号")
        logging.warning("还在测试中，可能存在较多问题，也可使用多账户模式运行")
        from task.game_task.one_account import one_account
        one_account()
    else:
        logging.error("配置文件错误：运行账号类别")
        sys.exit()
    #最后处理
    if originally_quality["flag"] == True:
        logging.info("正在恢复画质设置")
        reg_handler.write_reg_jsondata(winreg.HKEY_CURRENT_USER, r"Software\miHoYo\崩坏：星穹铁道", "GraphicsSettings_PCResolution_h431323223", "width", originally_quality["width"])
        reg_handler.write_reg_jsondata(winreg.HKEY_CURRENT_USER, r"Software\miHoYo\崩坏：星穹铁道", "GraphicsSettings_PCResolution_h431323223", "height", originally_quality["height"])
        reg_handler.write_reg_jsondata(winreg.HKEY_CURRENT_USER, r"Software\miHoYo\崩坏：星穹铁道", "GraphicsSettings_PCResolution_h431323223", "isFullScreen", originally_quality["isFullScreen"])
        reg_handler.write_reg_data(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\DirectX\UserGpuPreferences", os.path.normcase(config_handler("StarRail_path")), originally_quality["HDR"])
    if config_handler("over_control") == "poweroff":
        logging.info(f"将在1分钟后关机")
        time.sleep(60)
        os.system("shutdown /s /t 1")
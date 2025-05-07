import psutil
import subprocess
import logging

logger = logging.getLogger("process_handler")

class process_handler():
    def find_process(process_name):
        for proc in psutil.process_iter():
            try:
                if process_name.lower() in proc.name().lower():
                    return True
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        return False
    def kill_process(process_name):
        try:
            subprocess.Popen(["taskkill", "/f", "/im", process_name])
            logging.debug(f"已结束进程{process_name}")
            return True
        except:
            logging.error(f"结束进程{process_name}失败")
            return False
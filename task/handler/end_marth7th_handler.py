from task.handler.process_handler import process_handler
from task.handler.excel_handler import excel_handler
from task.handler.time_handler import nowtime

def end_march7th_handler(id,state):
    if state == "完成":
        excel_handler.write_excel(id, nowtime(), state)
        process_handler.kill_process("March7th Assistant.exe")
        process_handler.kill_process("PaddleOCR-json.exe")
    elif state == "超时":
        excel_handler.write_excel(id, nowtime(), state)
        process_handler.kill_process("StarRail.exe")
        process_handler.kill_process("March7th Assistant.exe")
        process_handler.kill_process("PaddleOCR-json.exe")
    elif state == "顶号":
        excel_handler.write_excel(id, nowtime(), state)
        process_handler.kill_process("StarRail.exe")
        process_handler.kill_process("March7th Assistant.exe")
        process_handler.kill_process("PaddleOCR-json.exe")
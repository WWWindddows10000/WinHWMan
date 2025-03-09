import win32print
import wmi
from PySide6.QtCore import QObject, Signal

class PrinterChecker(QObject):
    # 定义信号用于传递打印机状态
    printers_updated = Signal(list)

    def __init__(self):
        super().__init__()
        self.wmi_conn = wmi.WMI()

    def get_printer_status(self, printer_name):
        """通过 WMI 获取打印机状态码"""
        try:
            printers = self.wmi_conn.Win32_Printer(Name=printer_name)
            if printers:
                return printers[0].PrinterStatus
            return None
        except Exception as e:
            print(f"WMI 查询错误: {e}")
            return None

    def get_all_printers(self):
        """获取所有打印机及其状态"""
        printers = []
        try:
            # 获取所有打印机
            raw_printers = win32print.EnumPrinters(
                win32print.PRINTER_ENUM_LOCAL | win32print.PRINTER_ENUM_CONNECTIONS
            )
            
            # 获取默认打印机
            default_printer = win32print.GetDefaultPrinter()

            for printer in raw_printers:
                name = printer[2]
                is_default = (name == default_printer)
                status_code = self.get_printer_status(name)
                
                # 转换为状态文本
                status_map = {
                    1: "空闲",
                    2: "打印中",
                    3: "错误",
                    4: "离线",
                    5: "缺纸",
                    None: "未知状态"
                }
                status = status_map.get(status_code, "未知状态")
                
                printers.append({
                    "name": name,
                    "default": is_default,
                    "status": status,
                    "online": status_code not in [3, 4, None]
                })
        except Exception as e:
            print(f"打印机检测错误: {e}")
        
        return printers

    def check_printers(self):
        """执行检测并发射信号"""
        printers = self.get_all_printers()
        self.printers_updated.emit(printers)
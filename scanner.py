# ==================== 静默扫描模块 ====================
# ver 1 3/8
# usage: scanner = SilentScanner() scanner.scan()
# 保存路径：目前目录scanned.jpg

import win32com.client
import os
SCAN_CONFIG = {
    "scanner_name": "默认扫描仪",
    "resolution": 600,
    "color_mode": 1,
    "output_path": "scanned.jpg"
}

BARCODE_CONFIG = {
    "narrow_width": 2,    # 窄条2mm
    "wide_width": 4,      # 宽条4mm
    "height": 20,         # 条码高度20mm
    "dpi": 600,           
    "quiet_zone": 5       # 静区5mm
}


class SilentScanner:
    def __init__(self):
        self.device = None
        self._connect()
    
    def _connect(self):
        try:
            mgr = win32com.client.Dispatch("WIA.DeviceManager")
            if mgr.DeviceInfos.Count == 0:
                raise Exception("未检测到扫描设备")
            
            # 自动选择第一个设备
            self.device = mgr.DeviceInfos[1].Connect()
        except Exception as e:
            print(f"扫描仪连接失败: {e}")


    def scan(self):
        if not self.device:
            return False
        
        try:
            item = self.device.Items[1]
            img = item.Transfer()
            
            if img:
                if os.path.exists(SCAN_CONFIG["output_path"]):
                    os.remove(SCAN_CONFIG["output_path"])
                img.SaveFile(SCAN_CONFIG["output_path"])
                return True
        except Exception as e:
            print(f"扫描失败: {e}")
        return False
    
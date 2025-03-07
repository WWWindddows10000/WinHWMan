import cv2
import numpy as np
from PIL import Image, ImageDraw
import zlib
import win32com.client
import os

# ==================== 系统配置 ====================
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

# ==================== 唯一编码表 ====================
ENCODING_TABLE = {
    # 基础字符（4位）
    '0': '0000', '1': '0001', '2': '0010', '3': '0011',
    '4': '0100', '5': '0101', '6': '0110', '7': '0111',
    '8': '1000', '9': '1001', '-': '1010', '.': '1011',
    
    # 特殊代码（5位）
    'ZH':   '11000', 'MAT':  '11001', 'ENG':  '11010',
    'PHYSNR':'11011', 'PHYGK':'11100', 'BIO': '11101',
    'CEM':  '11110', 'CG':   '11111', 'RH':   '10000',
    'ZC':   '10001', 'TS':   '10010', 'WY':   '10011',
    'DT':   '10100', 'YD':   '10101', 'WB':   '10110',
    'BJ':   '10111', 'CT':   '10100', 'WS':   '10101'
}

DECODING_TABLE = {v:k for k,v in ENCODING_TABLE.items()}

# ==================== 静默扫描模块 ====================
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

    def _configure(self, item):
        try:
            props = item.Properties
            props["6147"].Value = SCAN_CONFIG["color_mode"]  # 颜色模式
            props["6146"].Value = SCAN_CONFIG["resolution"]  # 水平分辨率
            props["6148"].Value = SCAN_CONFIG["resolution"]  # 垂直分辨率
            props["6151"].Value = 0  # 关闭自动裁切
            props["6156"].Value = 1  # 禁用进度UI
        except Exception as e:
            print(f"参数设置失败: {e}")

    def scan(self):
        if not self.device:
            return False
        
        try:
            item = self.device.Items[1]
            self._configure(item)
            img = item.Transfer()
            
            if img:
                if os.path.exists(SCAN_CONFIG["output_path"]):
                    os.remove(SCAN_CONFIG["output_path"])
                img.SaveFile(SCAN_CONFIG["output_path"])
                return True
        except Exception as e:
            print(f"扫描失败: {e}")
        return False

# ==================== 条码生成模块 ====================
def mm_to_pixels(mm, dpi):
    return int(mm * dpi / 25.4)

def generate_barcode(data, output_file="barcode.png"):
    cfg = BARCODE_CONFIG
    narrow_px = mm_to_pixels(cfg["narrow_width"], cfg["dpi"])
    wide_px = mm_to_pixels(cfg["wide_width"], cfg["dpi"])
    height_px = mm_to_pixels(cfg["height"], cfg["dpi"])
    quiet_zone_px = mm_to_pixels(cfg["quiet_zone"], cfg["dpi"])
    
    # 编码数据
    buffer = str(data)
    encoded_bits = []
    while buffer:
        matched = False
        # 优先匹配最长特殊代码（6字符）
        for length in range(6, 0, -1):
            if length > len(buffer):
                continue
            candidate = buffer[:length]
            if candidate in ENCODING_TABLE:
                code = ENCODING_TABLE[candidate]
                encoded_bits.append(code)
                buffer = buffer[length:]
                matched = True
                break
        if not matched:
            encoded_bits.append(ENCODING_TABLE[buffer[0]])
            buffer = buffer[1:]
    
    # 添加校验码（CRC32）
    crc = zlib.crc32(data.encode()) & 0xFFFFFFFF
    encoded_bits.append(f"{crc:032b}"[:8])  # 取前8位
    
    # 构建完整编码流
    sync_code = '10101010'  # 同步头
    end_code = '01010101'   # 同步尾
    full_code = sync_code + ''.join(encoded_bits) + end_code
    
    # 生成图像
    total_width = quiet_zone_px * 2
    for bit in full_code:
        total_width += wide_px if bit == '1' else narrow_px
    
    img = Image.new("L", (total_width, height_px), 255)
    draw = ImageDraw.Draw(img)
    
    x = quiet_zone_px
    for bit in full_code:
        bar_width = wide_px if bit == '1' else narrow_px
        draw.rectangle([x, 0, x + bar_width, height_px], fill=0)
        x += bar_width
    
    img.save(output_file)
    print(f"条码已生成：{output_file}")

# ==================== 条码识别模块 ====================
class BarcodeDecoder:
    def __init__(self):
        self.sync_pattern = [1,0,1,0,1,0,1,0]
        self.end_pattern = [0,1,0,1,0,1,0,1]
    
    def _preprocess(self, img):
        # 自适应预处理
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
        enhanced = clahe.apply(gray)
        _, thresh = cv2.threshold(enhanced, 0, 255, 
                                cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        return thresh
    
    def _locate_barcode(self, img):
        # 投影分析定位
        proj = np.sum(img // 255, axis=0)
        edges = np.where(np.diff(proj > np.max(proj)//2))[0]
        if len(edges) < 2:
            return None
        return img[:, edges[0]:edges[-1]]
    
    def _decode_bits(self, roi):
        # 动态宽度分析
        scanline = np.mean(roi, axis=0)
        binary = (scanline < np.mean(scanline)*0.7).astype(int)
        
        # 查找同步码
        start = self._find_pattern(binary, self.sync_pattern)
        end = self._find_pattern(binary, self.end_pattern, reverse=True)
        if start is None or end is None:
            return None
        
        return binary[start+len(self.sync_pattern):end]
    
    def _find_pattern(self, arr, pattern, reverse=False):
        arr_str = ''.join(map(str, arr))
        target = ''.join(map(str, pattern))
        if reverse:
            pos = arr_str[::-1].find(target[::-1])
            return len(arr) - pos - len(pattern) if pos != -1 else None
        else:
            return arr_str.find(target)
    
    def decode(self, img_path):
        img = cv2.imread(img_path)
        if img is None:
            return None
        
        processed = self._preprocess(img)
        roi = self._locate_barcode(processed)
        if roi is None:
            return None
        
        bits = self._decode_bits(roi)
        if bits is None:
            return None
        
        # 分组解码
        buffer = ''.join(map(str, bits))
        result = []
        while len(buffer) >= 4:
            # 尝试5位解码
            if len(buffer) >=5 and buffer[:5] in DECODING_TABLE:
                result.append(DECODING_TABLE[buffer[:5]])
                buffer = buffer[5:]
            # 尝试4位解码
            elif buffer[:4] in DECODING_TABLE:
                result.append(DECODING_TABLE[buffer[:4]])
                buffer = buffer[4:]
            else:
                buffer = buffer[1:]  # 滑动窗口
        
        return ''.join(result)

# ==================== 主程序 ====================
if __name__ == "__main__":
    # 生成测试条码
    generate_barcode("BJ-PHYGK-5.1", "sample_barcode.png")
    
    # 自动扫描流程
    scanner = SilentScanner()
    if scanner.scan():
        # 解码条码
        decoder = BarcodeDecoder()
        result = decoder.decode(SCAN_CONFIG["output_path"])
        
        if result:
            print(f"解码成功：{result}")
        else:
            print("解码失败")
    else:
        print("扫描失败")

    # 直接测试生成文件
    test_result = decoder.decode("sample_barcode.png")
    print(f"直接测试结果：{test_result}")
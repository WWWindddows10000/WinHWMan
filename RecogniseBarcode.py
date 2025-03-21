#弃用，改手写识别
import cv2
import numpy as np
import scanner as scan
# 读取图像
ENCODING_TABLE = {
    # 基础字符（4位）
    '0': '0000', '1': '0001', '2': '0010', '3': '1101',
    '4': '0100', '5': '0101', '6': '0110', '7': '0111',
    '8': '1000', '9': '1001', '-': '1010', '.': '1011',
    
    # 特殊代码（5位）
    'ZH':   '11000', 'MAT':  '11001', 'ENG':  '11010',
    'PHYSNR':'11011', 'PHYGK':'11100', 'BIO': '11101',
    'CEM':  '01001', 'CG':   '11111', 'RH':   '10000',
    'ZC':   '10001', 'TS':   '10010', 'WY':   '10011',
    'DT':   '00101', 'YD':   '10101', 'WB':   '10110',
    'BJ':   '10111', 'CT':   '10100', 'WS':   '01100',

    #起始终止
    "start":  '11110',"end":   "01111"
    }

DECODING_TABLE = {v:k for k,v in ENCODING_TABLE.items()}

def recognise(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # 改进1：使用闭操作连接条码区域
    binary = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                  cv2.THRESH_BINARY_INV, 21, 5)  # 增大块大小
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    closed = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel, iterations=3)
    
    # 改进2：直接使用二值化图像找轮廓（而非Canny）
    contours, _ = cv2.findContours(closed, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    
    # 改进3：动态合并相邻轮廓
    merged_contours = []
    prev_x, prev_y, prev_w, prev_h = -999, -999, 0, 0  # 初始值
    for cnt in sorted(contours, key=lambda c: cv2.boundingRect(c)[0]):  # 按x坐标排序
        x, y, w, h = cv2.boundingRect(cnt)
        
        # 水平合并条件：相邻区域间隔小于20像素且高度重叠
        if (x - (prev_x + prev_w) < 20) and (abs(y - prev_y) < 0.3 * max(h, prev_h)):
            prev_w = x + w - prev_x
            prev_h = max(prev_h, y + h - prev_y)
        else:
            if prev_w > 0:
                merged_contours.append((prev_x, prev_y, prev_w, prev_h))
            prev_x, prev_y, prev_w, prev_h = x, y, w, h
    if prev_w > 0:
        merged_contours.append((prev_x, prev_y, prev_w, prev_h))
    
    # 筛选条件优化
    barcode_contours = []
    top_threshold_pixels = 24
    for (x, y, w, h) in merged_contours:
        aspect_ratio = w / h
        # 放宽长宽比限制，增加垂直方向判断
        if (aspect_ratio > 1.2 or h / w > 1.2) and y > top_threshold_pixels and w > 20:
            barcode_contours.append((x, y, w, h))
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
    
    return barcode_contours

def mm_to_pixels(mm, dpi=300):
    """将毫米转换为像素（默认300 DPI）"""
    return int(mm * dpi / 25.4)

def decode_barcodes(areas, image, dpi=300):
    """
    处理多个候选区域，返回首个有效条码数据
    :param areas: 候选区域列表 [(x,y,w,h), ...]
    :param image: 原始BGR图像
    :param dpi: 图像分辨率（默认300）
    :return: 首个有效条码中间数据 或 None
    """
    # 预处理全局图像
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)
    
    for (x, y, w, h) in areas:
        # 提取ROI并转换为0-1数组
        roi = binary[y:y+h, x:x+w]
        roi_bin = (roi // 255).astype(np.uint8)
        
        # 获取二进制序列（优化版本）
        binary_str = extract_binary_sequence(roi_bin, dpi)
        
        # 解码并验证格式
        try:
            decoded = decode_custom_barcode(binary_str, DECODING_TABLE)
            print(decoded)
            # if decoded.startswith("start") and decoded.endswith("end"):
            #     return decoded[5:-3]  # 去除start(5)和end(3)
        except ValueError:
            continue
    
    return None  # 无有效条码

def extract_binary_sequence(roi_bin, dpi):
    """
    从ROI中提取可靠的二进制序列（改进版）
    """
    # 使用多行采样提高鲁棒性
    height, width = roi_bin.shape
    sampled_rows = [
        roi_bin[int(height*0.3), :],  # 上采样区
        roi_bin[height//2, :],        # 中心线
        roi_bin[int(height*0.7), :]   # 下采样区
    ]
    
    # 动态计算允许的像素宽度
    min_width = max(1, mm_to_pixels(0.8, dpi))
    max_width = mm_to_pixels(1.2, dpi)
    
    # 三线投票机制
    candidates = []
    for row in sampled_rows:
        seq = []
        prev_val = row[0]
        count = 1
        for val in row[1:]:
            if val == prev_val:
                count += 1
            else:
                # 合并过窄的条（小于0.8mm视为噪声）
                if count >= min_width:
                    seq.append((prev_val, count))
                prev_val = val
                count = 1
        seq.append((prev_val, count))
        
        # 转换为二进制字符串（考虑宽度容差）
        bin_str = ""
        for val, width in seq:
            if min_width <= width <= max_width:
                bin_str += '1' if val else '0'
        candidates.append(bin_str)
    
    # 选择最长的有效序列
    return max(candidates, key=len)

# 复用之前的解码函数（需稍作调整）
def decode_custom_barcode(binary_str, decoding_table):
    result = []
    i = 0
    n = len(binary_str)
    while i < n:
        # 优先匹配5位
        if i+5 <= n and (code := decoding_table.get(binary_str[i:i+5])):
            result.append(code)
            i +=5
        # 次优匹配4位
        elif i+4 <=n and (code := decoding_table.get(binary_str[i:i+4])):
            result.append(code)
            i +=4
        else:
            # 允许跳过无法解码的部分（提高容错性）
            i +=1
    return "".join(result)


def decode(image):
    area = recognise(image)
    res = decode_barcodes(area, image)
    print(res)
    return res

# scanner = scan.SilentScanner()
# scanner.scan()
# image = cv2.imread('scanned.jpg')
# decode(image)
# cv2.imshow('Detected Barcode', image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
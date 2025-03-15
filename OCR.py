import cv2 
from paddleocr import PaddleOCR
import scanner as scan
import numpy as np
from PIL import Image



def extract_ocr_text(result):
    texts = []
    for item in result:
        if isinstance(item, list):
            texts.extend(extract_ocr_text(item))
        # 如果当前元素是包含文字信息的元组（文本，置信度）
        elif isinstance(item, tuple) and len(item) >= 2:
            if isinstance(item[0], str):  # 确保第一个元素是文本
                texts.append(item[0])
        elif isinstance(item, list) and len(item) >= 2:
            if isinstance(item[1], tuple):
                texts.append(item[1][0])
    return texts

def scanOcr():
    ocr = PaddleOCR(use_angle_cls=True, lang='ch')
    scanner = scan.SilentScanner()
    scanner.scan()
    # OCR识别
    # 定义转换函数：厘米转像素（DPI300）
    def cm_to_pixels(cm, dpi=300):
        return int(cm * dpi / 2.54)

    # 读取图像
    img = cv2.imread('scanned.jpg')
    height, width = img.shape[:2]

    # 计算目标区域的像素尺寸
    target_width_px = cm_to_pixels(5.5)  # 1.5cm宽度
    target_height_px = cm_to_pixels(1.5) # 5.5cm高度

    # 计算右上角坐标（从右上角向左下方取区域）
    x_start = width - target_width_px
    y_end = target_height_px

    # 裁剪区域（确保坐标不越界）
    cropped = img[0:y_end, max(0, x_start):width]

    # 转换颜色空间BGR→RGB，并创建Pillow对象
    pil_image = Image.fromarray(cv2.cvtColor(cropped, cv2.COLOR_BGR2RGB))

    # 保存图像并设置DPI
    pil_image.save('scanned2.jpg', dpi=(300, 300), quality=95)

    print(f"裁剪保存完成，尺寸：{cropped.shape[1]}x{cropped.shape[0]}像素")
    result = ocr.ocr('scanned2.jpg', cls=True)

    # 提取并打印所有文本
    all_texts = extract_ocr_text(result)
    return all_texts[0].split('\n')[0]+'-1'

def ScanPage(FID,page):
    scanner = scan.SilentScanner()
    scanner.scan()
    return "{}-{}".format(FID,page)
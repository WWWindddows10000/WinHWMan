import win32com.client
import os

def scan_with_wia(output_path="scan_output.jpg"):
    try:
        # 创建 WIA 对象
        wia = win32com.client.Dispatch("WIA.CommonDialog")
        img = wia.ShowAcquireImage(
            FormatID="{B96B3CAE-0728-11D3-9D7B-0000F81EF32E}",  # JPEG 格式
            Intent=0x0004,  # 彩色扫描
            Bias=0x00020000  # 高分辨率
        )
        
        if img:
            # 保存扫描结果
            img.SaveFile(output_path)
            print(f"扫描完成，文件保存至: {os.path.abspath(output_path)}")
        else:
            print("扫描取消或失败。")
    except Exception as e:
        print(f"发生错误: {e}")

if __name__ == "__main__":
    scan_with_wia()
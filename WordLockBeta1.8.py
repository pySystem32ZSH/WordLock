import time
import tkinter as tk
from tkinter import scrolledtext

bits16 = ['0000','0001','0010','0011','0100','0101','0110','0111','1000','1001','1010','1011','1100','1101','1110','1111']
bits16word = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P']

# 加解密核心
def text_to_bits(text):
    bytes_data = text.encode('utf-8')
    return ''.join(format(byte, '08b') for byte in bytes_data)

def bits_to_text(bits):
    if len(bits) % 8 != 0:
        raise ValueError("二进制长度必须是8的倍数")
    bytes_list = []
    for i in range(0, len(bits), 8):
        byte = bits[i:i+8]
        bytes_list.append(int(byte, 2))
    bytes_data = bytes(bytes_list)
    return bytes_data.decode('utf-8')

def bits_to_bits16(bits):
    remainder = len(bits) % 4
    if remainder != 0:
        bits = bits + '0' * (4 - remainder)
    result = []
    for i in range(0, len(bits), 4):
        four_bits = bits[i:i+4]
        index = bits16.index(four_bits)
        result.append(bits16word[index])
    return ''.join(result)

def bits16_to_bits(bits_str):
    res = []
    for c in bits_str:
        if c not in bits16word:
            raise ValueError(f"无效字符：{c}，仅支持A-P")
        res.append(bits16[bits16word.index(c)])
    return ''.join(res)

def reverse_bits(bits):
    return bits[::-1]

def invert_bits(bits):
    return ''.join('1' if b == '0' else '0' for b in bits)

def encrypt(plaintext):
    bits = text_to_bits(plaintext)
    reversed_bits = reverse_bits(bits)
    encrypted_bits = invert_bits(reversed_bits)
    return bits_to_bits16(encrypted_bits)

def decrypt(encrypted_str):
    bits_from_16 = bits16_to_bits(encrypted_str)
    inverted_bits = invert_bits(bits_from_16)
    original_bits = reverse_bits(inverted_bits)
    while len(original_bits) % 8 != 0:
        if original_bits[-1] != '0':
            break
        original_bits = original_bits[:-1]
    return bits_to_text(original_bits)

# 全局窗口尺寸配置
MAIN_W = 400
MAIN_H = 220
INPUT_W = 520
INPUT_H = 280
RESULT_W = 750
RESULT_H = 450
MSG_W = 380
MSG_H = 180

FONT_NORMAL = ("Microsoft YaHei", 11)
FONT_TITLE  = ("Microsoft YaHei", 12, "bold")
FONT_CODE   = ("Consolas", 11)

# 统一居中函数
def center_win(win, w, h):
    win.geometry(f"{w}x{h}")
    win.update_idletasks()
    x = (win.winfo_screenwidth() - w) // 2
    y = (win.winfo_screenheight() - h) // 2
    win.geometry(f"{w}x{h}+{x}+{y}")
    win.resizable(False, False)

# 消息提示窗
def show_msg(title, text):
    win = tk.Toplevel()
    win.title(title)
    center_win(win, MSG_W, MSG_H)
    tk.Label(win, text=text, font=FONT_NORMAL, wraplength=320).pack(expand=True)
    tk.Button(win, text="确定", command=win.destroy, font=FONT_NORMAL, width=8).pack(pady=10)

# 输出结果
def show_result(title, content):
    win = tk.Toplevel()
    win.title(title)
    center_win(win, RESULT_W, RESULT_H)
    txt = scrolledtext.ScrolledText(win, font=FONT_CODE)
    txt.pack(expand=True, fill=tk.BOTH, padx=15, pady=15)
    txt.insert(tk.END, content)
    txt.config(state=tk.DISABLED)
    tk.Button(win, text="关闭", command=win.destroy, font=FONT_NORMAL).pack(pady=5)

# 加密
def open_encrypt_input():
    win = tk.Toplevel()
    win.title("加密操作 - 请输入明文")
    center_win(win, INPUT_W, INPUT_H)

    tk.Label(win, text="请输入要加密的明文：", font=FONT_TITLE).pack(pady=10)
    entry = tk.Text(win, font=FONT_CODE, width=50, height=6)
    entry.pack(padx=20)

    def confirm():
        content = entry.get("1.0", tk.END).strip()
        if not content:
            show_msg("提示", "明文不能为空！")
            return
        try:
            res = encrypt(content)
            win.destroy()
            show_result("加密结果", f"加密成功！结果如下：\n\n{res}")
        except Exception as e:
            show_msg("错误", f"加密失败：{e}")

    frm = tk.Frame(win)
    frm.pack(pady=12)
    tk.Button(frm, text="确认加密", command=confirm, font=FONT_NORMAL, width=10).grid(row=0,column=0,padx=10)
    tk.Button(frm, text="取消", command=win.destroy, font=FONT_NORMAL, width=10).grid(row=0,column=1,padx=10)

# 解密
def open_decrypt_input():
    win = tk.Toplevel()
    win.title("解密操作 - 请输入密文")
    center_win(win, INPUT_W, INPUT_H)

    tk.Label(win, text="请输入要解密的密文(仅A-P)：", font=FONT_TITLE).pack(pady=10)
    entry = tk.Text(win, font=FONT_CODE, width=50, height=6)
    entry.pack(padx=20)

    def confirm():
        content = entry.get("1.0", tk.END).strip().upper()
        if not content:
            show_msg("提示", "密文不能为空！")
            return
        try:
            res = decrypt(content)
            win.destroy()
            # 彩蛋
            if res.strip() == "250":
                show_msg("彩蛋界面", "注意：检测到高危文字")
                time.sleep(5)
            elif res.strip() == "520":
                show_msg("彩蛋界面", "注意：检测到爱情线")
                time.sleep(5)
            show_result("解密结果", f"解密成功！原始明文如下：\n\n{res}")
        except UnicodeDecodeError:
            show_msg("错误", "解密失败：无法解码为有效文本，请检查密文！")
        except Exception as e:
            show_msg("错误", f"解密失败：{e}")

    frm = tk.Frame(win)
    frm.pack(pady=12)
    tk.Button(frm, text="确认解密", command=confirm, font=FONT_NORMAL, width=10).grid(row=0,column=0,padx=10)
    tk.Button(frm, text="取消", command=win.destroy, font=FONT_NORMAL, width=10).grid(row=0,column=1,padx=10)

# 主界面
def main():
    root = tk.Tk()
    root.title("特殊信息加密解密工具-Beta1.8")
    center_win(root, MAIN_W, MAIN_H)

    tk.Button(root, text="加密", command=open_encrypt_input, font=FONT_NORMAL, width=10, height=2)\
        .place(relx=0.5, rely=0.18, anchor=tk.CENTER)
    tk.Button(root, text="解密", command=open_decrypt_input, font=FONT_NORMAL, width=10, height=2)\
        .place(relx=0.5, rely=0.48, anchor=tk.CENTER)
    tk.Button(root, text="退出", command=lambda:(root.quit(), show_msg("退出", "感谢使用，再见！")), font=FONT_NORMAL, width=10, height=2)\
        .place(relx=0.5, rely=0.78, anchor=tk.CENTER)

    root.mainloop()

if __name__ == "__main__":
    main()
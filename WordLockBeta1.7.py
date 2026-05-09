import easygui

bits16 = ['0000','0001','0010','0011','0100','0101','0110','0111','1000','1001','1010','1011','1100','1101','1110','1111']
bits16word = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P']

def text_to_bits(text): #UTF-8加密
    bytes_data = text.encode('utf-8')
    return ''.join(format(byte, '08b') for byte in bytes_data)

def bits_to_text(bits): #UTF-8解码
    if len(bits) % 8 != 0:
        raise ValueError("二进制长度必须是8的倍数")
    
    bytes_list = []
    for i in range(0, len(bits), 8):
        byte = bits[i:i+8]
        bytes_list.append(int(byte, 2))
    
    bytes_data = bytes(bytes_list)
    return bytes_data.decode('utf-8')

def bits_to_bits16(bits): #字符串转字母
    remainder = len(bits) % 4
    if remainder != 0:
        bits = bits + '0' * (4 - remainder)  #补0使长度为4的倍数
    result = []
    for i in range(0, len(bits), 4):
        four_bits = bits[i:i+4]
        index = bits16.index(four_bits)
        result.append(bits16word[index])
    return ''.join(result)

def bits16_to_bits(bits_str): #字母转二进制
    res = []
    for c in bits_str:
        if c not in bits16word:
            raise ValueError(f"无效字符：{c}，仅支持A-P")
        res.append(bits16[bits16word.index(c)])
    return ''.join(res)

def reverse_bits(bits): #颠倒字符串
    return bits[::-1]

def invert_bits(bits): #二进制取反
    return ''.join('1' if b == '0' else '0' for b in bits)

def encrypt(plaintext):
    bits = text_to_bits(plaintext)
    reversed_bits = reverse_bits(bits)
    encrypted_bits = invert_bits(reversed_bits)
    encrypted_16word = bits_to_bits16(encrypted_bits)
    return encrypted_16word

def decrypt(encrypted_str):
    #字母转二进制
    bits_from_16 = bits16_to_bits(encrypted_str)
    #对二进制取反
    inverted_bits = invert_bits(bits_from_16)
    #反转二进制
    original_bits = reverse_bits(inverted_bits)
    #去除加密时补的0
    while len(original_bits) % 8 != 0:
        #从末尾移除加密时补的0（最多移除3个）
        if original_bits[-1] != '0':
            break
        original_bits = original_bits[:-1]
    #二进制转文本
    return bits_to_text(original_bits)

def main():
    while True:
        choice = easygui.buttonbox(
            "请选择操作：",
            "特殊信息加密解密工具-Beta1.7",
            ["加密", "解密", "退出"]
        )
        
        if choice == "退出" or choice is None:
            easygui.msgbox("感谢使用，再见！", "退出")
            break
        
        elif choice == "加密":
            plaintext = easygui.enterbox(
                "请输入要加密的明文：",
                "加密操作"
            )
            if plaintext is None:
                continue
            
            if plaintext == "":
                easygui.msgbox("明文不能为空！", "错误")
                continue
            
            try:
                encrypted = encrypt(plaintext)
                easygui.codebox(
                    "加密成功！结果如下：",
                    "加密结果",
                    encrypted
                )
            except Exception as e:
                easygui.msgbox(f"加密失败：{str(e)}", "错误")
        
        elif choice == "解密":
            encrypted = easygui.enterbox(
                f"请输入要解密的密文：",
                "解密操作"
            )
            if encrypted is None:
                continue
            
            encrypted = encrypted.strip().upper()  #转大写，去空格
            if encrypted == "":
                easygui.msgbox("密文不能为空！", "错误")
                continue
            
            try:
                decrypted = decrypt(encrypted)
                #彩蛋
                if decrypted.strip() == "250":
                    easygui.msgbox(title="彩蛋界面", msg="注意：检测到高危文字")
                if decrypted.strip() == "520":
                    easygui.msgbox(title="彩蛋界面", msg="注意：检测到爱情线")
                easygui.codebox(
                    "解密成功！原始明文如下：",
                    "解密结果",
                    decrypted
                )
            except UnicodeDecodeError:
                easygui.msgbox("解密失败：无法将结果解码为有效的UTF-8文本。\n请检查密文是否正确。", "错误")
            except ValueError as e:
                easygui.msgbox(f"解密失败：{str(e)}", "错误")
            except Exception as e:
                easygui.msgbox(f"解密失败：{str(e)}", "错误")

if __name__ == "__main__":
    main()
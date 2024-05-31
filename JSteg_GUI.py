import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import cv2

def text_to_bits(text, encoding='latin-1'):
    # 将文本转换为比特流
    bits = bin(int.from_bytes(text.encode(encoding), 'big'))[2:]
    return bits.zfill(8 * ((len(bits) + 7) // 8))

def bits_to_text(bits, encoding='latin-1'):
    # 将比特流转换回文本
    n = int(bits, 2)
    return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode(encoding)

def hide_message(image_path, message):
    # 读取图像
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError("无法读取图像文件")

    height, width, _ = image.shape
    # 将消息转换为比特流
    message_bits = text_to_bits(message)
    message_length = len(message_bits)

    if message_length > height * width * 3:
        raise ValueError("消息太长，无法隐藏在图像中")

    message_index = 0
    for i in range(height):
        for j in range(width):
            for k in range(3):
                if message_index < message_length:
                    binary_pixel = bin(image[i, j, k])[2:].zfill(8)
                    modified_pixel = binary_pixel[:-1] + message_bits[message_index]
                    image[i, j, k] = int(modified_pixel, 2)
                    message_index += 1
                else:
                    break

    # 保存带有隐藏信息的图像
    cv2.imwrite('hidden_image.png', image)
    messagebox.showinfo("成功", "消息成功隐藏")

def extract_message(image_path):
    # 读取带有隐藏信息的图像
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError("无法读取图像文件")

    height, width, _ = image.shape
    extracted_bits = ''
    for i in range(height):
        for j in range(width):
            for k in range(3):
                binary_pixel = bin(image[i, j, k])[2:].zfill(8)
                extracted_bits += binary_pixel[-1]

    # 将提取的比特流转换为文本消息
    extracted_message = bits_to_text(extracted_bits)
    return extracted_message

def browse_image():
    filename = filedialog.askopenfilename(title="选择图像")
    entry_image.delete(0, tk.END)
    entry_image.insert(0, filename)

def hide():
    image_path = entry_image.get()
    message = entry_message.get()
    try:
        hide_message(image_path, message)
    except Exception as e:
        messagebox.showerror("错误", str(e))

def extract():
    image_path = entry_image.get()
    try:
        extracted_message = extract_message(image_path)
        messagebox.showinfo("提取的消息", f"提取的消息：{extracted_message}")
    except Exception as e:
        messagebox.showerror("错误", str(e))

# 创建 GUI 窗口
root = tk.Tk()
root.title("隐写术工具")

# 创建输入部件
label_image = tk.Label(root, text="选择图像:")
entry_image = tk.Entry(root, width=50)
button_browse = tk.Button(root, text="浏览", command=browse_image)

label_message = tk.Label(root, text="消息:")
entry_message = tk.Entry(root, width=50)

button_hide = tk.Button(root, text="隐藏消息", command=hide)
button_extract = tk.Button(root, text="提取消息", command=extract)

# 将部件放入窗口
label_image.grid(row=0, column=0, padx=5, pady=5)
entry_image.grid(row=0, column=1, padx=5, pady=5)
button_browse.grid(row=0, column=2, padx=5, pady=5)

label_message.grid(row=1, column=0, padx=5, pady=5)
entry_message.grid(row=1, column=1, padx=5, pady=5)

button_hide.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="ew")
button_extract.grid(row=2, column=2, padx=5, pady=5, sticky="ew")

root.mainloop()
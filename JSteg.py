import cv2

def text_to_bits(text, encoding='latin-1'):
    bits = bin(int.from_bytes(text.encode(encoding), 'big'))[2:]
    return bits.zfill(8 * ((len(bits) + 7) // 8))

def bits_to_text(bits, encoding='latin-1'):
    n = int(bits, 2)
    return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode(encoding)

def hide_message(image_path, message):
    # 读取图像
    image = cv2.imread(image_path)
    
    if image is None:
        raise FileNotFoundError("不能读取到图片，请重新检查图片路径")

    height, width, _ = image.shape

    # 将消息转换为比特流
    message_bits = text_to_bits(message)
    message_length = len(message_bits)

    if message_length > height * width * 3:
        raise ValueError("消息太长，请修改要隐藏的信息！")

    # 将消息嵌入图像的最低有效位中
    message_index = 0
    for i in range(height):
        for j in range(width):
            for k in range(3):  # 三个颜色通道：红、绿、蓝
                if message_index < message_length:
                    binary_pixel = bin(image[i, j, k])[2:].zfill(8)
                    modified_pixel = binary_pixel[:-1] + message_bits[message_index]
                    image[i, j, k] = int(modified_pixel, 2)
                    message_index += 1
                else:
                    break

    # 保存带有隐藏信息的图像
    cv2.imwrite('hidden_image.png', image)

def extract_message(image_path):
    # 读取带有隐藏信息的图像
    image = cv2.imread(image_path)
    
    if image is None:
        raise FileNotFoundError("Unable to read image file")

    height, width, _ = image.shape

    # 从图像中提取隐藏的消息
    extracted_bits = ''
    for i in range(height):
        for j in range(width):
            for k in range(3):
                binary_pixel = bin(image[i, j, k])[2:].zfill(8)
                extracted_bits += binary_pixel[-1]

    # 将提取的比特流转换为文本消息
    message = bits_to_text(extracted_bits)

    return message

# 测试代码
if __name__ == "__main__":
    # 隐藏消息
    hide_message('original_image.png', '20211207039') # 隐藏信息为 20211207039

    # 提取消息
    extracted_message = extract_message('hidden_image.png')
    print("提取到的隐藏信息为：", extracted_message)

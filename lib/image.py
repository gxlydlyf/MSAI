import PIL.Image
import colorama
import shutil

colorama.init()


def generate_ascii_art(image_path, width='auto', height='auto',
                       ascii_chars='█', chars_num=2, black_pixel='ascii_chars'):
    """
    Args:
        black_pixel(str): 黑色的像素
        chars_num (int): ascii_chars出现的次数
        image_path (str): 图片路径
        width (int,str): 宽度
        height (int,str): 高度
        ascii_chars (str): 图片字符

    """
    chars_num = int(chars_num)  # 转化整数
    # 打开图像文件
    image = PIL.Image.open(image_path)
    image_original_width = image.size[0]
    image_original_height = image.size[1]

    terminal_width, terminal_height = shutil.get_terminal_size()

    # 调整图像大小
    if width == 'auto':
        width = terminal_width / chars_num
    if height == 'auto':
        width = terminal_height
    if height == 'width':
        height = width

    if width == 'raw':
        width = image_original_width
    if height == 'raw':
        height = image_original_height

    if black_pixel == 'ascii_chars':
        black_pixel = ascii_chars

    width = int(width)
    height = int(height)

    image = image.resize((width, height))

    # 替换图像像素的字符集
    if not ascii_chars:
        ascii_chars = '@%#*+=-:. '  # 设置为随机字符

    def convert_pixel_to_char(pixel):
        r, g, b = pixel[:3]
        brightness = (0.299 * r + 0.587 * g + 0.114 * b) / 255
        choose_ascii_chars = ascii_chars
        if str(brightness) == "0.0":
            choose_ascii_chars = black_pixel
        char_index = int(brightness * (len(choose_ascii_chars) - 1))
        char = choose_ascii_chars[char_index]
        # Return ANSI escape sequence with RGB values
        return f"\033[38;2;{r};{g};{b}m{char * chars_num}"

    # Convert each pixel in the image to its corresponding character
    output = ''
    for y in range(image.size[1]):
        for x in range(image.size[0]):
            output += convert_pixel_to_char(image.getpixel((x, y)))  # 把某个像素点转化为字符
        output += '\n'  # 换行
    output += colorama.Fore.RESET  # 重置颜色

    return output


if __name__ == '__main__':
    # Example usage

    ascii_art = generate_ascii_art(
        'E:\\MinecraftMSAI\\icon\\icons8-minecraft-512.png',
        'auto',
        'width',
        black_pixel=' '
    )
    print(ascii_art)

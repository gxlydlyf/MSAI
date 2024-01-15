import colorama


def create_terminal(data, fg_color=None, bg_color=None, mode=None):
    color_map = {
        'black': 30, 'red': 31, 'green': 32, 'yellow': 33,
        'blue': 34, 'magenta': 35, 'cyan': 36, 'white': 37,
        '黑色': 30, '红色': 31, '绿色': 32, '黄色': 33,
        '蓝色': 34, '品红': 35, '青色': 36, '白色': 37
    }
    mode_map = {
        'reset': 0, 'bold': 1, 'dim': 2, 'underline': 4,
        'blink': 5, 'reverse': 7, 'hidden': 8,
        '重置': 0, '加粗': 1, '暗淡': 2, '下划线': 4,
        '闪烁': 5, '反转': 7, '隐藏': 8
    }
    # 初始化colorama库
    colorama.init()

    # 设置前景色
    if fg_color in color_map:
        fg_code = color_map[fg_color]
        data = f"\033[{fg_code}m{data}"
    elif isinstance(fg_color, int) and 0 <= fg_color <= 255:
        data = f"\033[38;5;{fg_color}m{data}"

    # 设置背景色
    if bg_color in color_map:
        bg_code = color_map[bg_color]
        data = f"\033[{bg_code + 10}m{data}"
    elif isinstance(bg_color, int) and 0 <= bg_color <= 255:
        data = f"\033[48;5;{bg_color}m{data}"

    # 设置显示模式
    if mode in mode_map:
        mode_code = mode_map[mode]
        data = f"\033[{mode_code}m{data}"

    # 重置颜色和显示模式
    data = f"{data}{colorama.Style.RESET_ALL}"

    return data

# 设置前景色为红色，背景色为蓝色，样式为下划线
# result = create_terminal("Hello World!", fg_color="red", bg_color="blue", mode="underline")
# print(result)
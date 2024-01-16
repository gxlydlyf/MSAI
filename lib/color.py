from colorama import init, Fore, Back, Style


def create_terminal(data, bg_color, fg_color, mode, print_text=False, reset_terminal=True):
    init()  # 初始化colorama库

    # 设置背景色
    if isinstance(bg_color, str):
        bg_color = getattr(Back, bg_color.upper(), Back.RESET)
    else:
        bg_color = Back.RESET

    # 设置前景色
    if isinstance(fg_color, str):
        fg_color = getattr(Fore, fg_color.upper(), Fore.RESET)
    else:
        fg_color = Fore.RESET

    # 设置终端模式
    if mode == 'bold':
        mode = Style.BRIGHT
    elif mode == 'underline':
        mode = '\033[4m'  # 使用ANSI转义序列设置下划线（因为colorama库的Style.UNDERLINE被废弃）
    else:
        mode = Style.NORMAL

    # 返回带有设置的文本
    formatted_text = f"{mode}{bg_color}{fg_color}{data}"
    if reset_terminal is True:
        formatted_text += Style.RESET_ALL
    if print_text is True:
        print(formatted_text)
    return formatted_text


if __name__ == "__main__":
    # 示例用法
    create_terminal("示例文本", "bold", "red", "white", print_text=True)  # 设置为粗体，红色背景，白色前景
    create_terminal("示例文本", "underline", "green", "black", print_text=True)  # 设置为下划线，蓝色背景，黄色前景

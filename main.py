# <a target="_blank" href="https://icons8.com/icon/XfjNd4vkhBBy/minecraft-grass-cube">Minecraft</a>
# 图标来自
# <a target="_blank" href="https://icons8.com">Icons8</a>
import os
import subprocess
import sys

import requests
from tqdm import tqdm
import zipfile
import datetime
import pytz
from tzlocal import get_localzone
import re
import socket
import threading
import win32api
import win32con
import psutil
from lib.color import create_terminal
from lib.system_bits import system_64_bits
from lib.system_bits import java_64_bits
from lib.simple_configuration import SimpleConfiguration
from lib.image import generate_ascii_art
import shutil
from art import text2art

version = "2.0.0.1"
try:
    def highlight_color(data):
        return create_terminal(data=data, fg_color="yellow", bg_color="black", mode="bold")


    def red_highlight_color(data):
        return create_terminal(data=data, fg_color="red", bg_color="black", mode="bold")


    def green_highlight_color(data):
        return create_terminal(data=data, fg_color=47, bg_color="green", mode="bold")


    def yellow_highlight_color(data):
        return create_terminal(data=data, fg_color=47, bg_color="yellow", mode="bold")


    print(create_terminal('', fg_color=47, bg_color="yellow", mode="bold", reset_terminal=False))
    print(generate_ascii_art(os.path.dirname(os.path.abspath(__file__))+'/icon/icons8-minecraft-512.png', height='width', black_pixel=' '))
    print(text2art(text='MSAI'))
    print(text2art("version:" + version))
    print("""
    项目:https://github.com/gxlydlyf/MSAI
    欢迎使用此启动器，如果您需要新功能或出现问题，请在 issues(https://github.com/gxlydlyf/MSAI/issues)寻求帮助！
    """)
    print(yellow_highlight_color(''))

    current_dir = os.getcwd()
    current_path = os.path.abspath(current_dir)
    print('当前目录：', highlight_color(current_path))
    deploy_path = current_path + "\\.MSAI"
    print('配置目录：', highlight_color(deploy_path))
    environment_path = deploy_path + "\\environment"
    print('环境目录：', highlight_color(environment_path))
    server_path = deploy_path + "\\server"
    print('服务器目录：', highlight_color(server_path))

    run_restart = 0

    user_config = SimpleConfiguration(
        {
            "#1": "这是“游戏版本”的配置，默认为1.20.4，您可以设置为其他的值",
            "游戏版本": "1.20.4",
            "#2": "这是“最大内存”的配置，可以设定服务器最大使用的内存(只能为整数)，默认为空(即无限制，32位系统限制1G)，以下设置效果相同(均为1024制)：\n"
                  "# “4G”(单位：GB)\n"
                  "# “4096M”(单位：MB)\n"
                  "# “4194304K”(单位：KB)\n"
                  "# “4294967296”(单位：bit)\n"
                  "# 您可在“https://www.toolhelper.cn/Digit/ByteCalc”进行单位换算",
            "最大内存": ""
        },
        absolute_path=deploy_path,
        file_name="启动器配置文件"
    )

    # https://api.papermc.io/v2/projects/paper/versions/1.20.4/builds/381/downloads/paper-1.20.4-381.jar 原版链接
    # https://kkgithub.com/gxlydlyf/MSAI/raw/master/file/paper-1.20.4-381.jar 使用了代理：https://kkgithub.com
    paperServerFile_path = \
        "https://raw.nuaa.cf/gxlydlyf/MSAI/master/file/paper-1.20.4-385.jar"  # 使用了代理：https://hub.nuaa.cf
    print('Paper服务器文件下载地址：', highlight_color(paperServerFile_path))

    serverFile_path = server_path + "\\server.jar"
    print('服务器启动文件路径：', highlight_color(serverFile_path))
    eulaFile_path = server_path + "\\eula.txt"
    print('eula文件路径：', highlight_color(eulaFile_path))
    serverProperties_path = server_path + "\\server.properties"
    print('server.properties文件路径：', highlight_color(serverProperties_path))
    serverLog_path = deploy_path + "\\logs"
    print('服务器日志文件路径：', highlight_color(serverLog_path))

    jdkDir_path = environment_path + "\\jdk17"
    print('Jdk文件路径：', highlight_color(jdkDir_path))
    javaFile_path = jdkDir_path + "\\bin\\java.exe"
    print('Java文件路径：', highlight_color(javaFile_path))
    jarFile_path = jdkDir_path + "\\bin\\jar.exe"
    print('Jar文件路径：', highlight_color(jarFile_path))
    javaZip_path = environment_path + "\\jdk17.zip"
    print('JavaZip文件路径：', highlight_color(javaZip_path))


    def show_message_box(message, title):
        def show_message_box_():
            win32api.MessageBox(0, message, title, win32con.MB_ICONINFORMATION)

        message_thread = threading.Thread(target=show_message_box_)
        message_thread.start()


    def delete_folder(folder_path):
        try:
            # 删除文件夹
            shutil.rmtree(folder_path)
            # print("文件夹删除成功")
            return True
        except OSError:
            # print(f"文件夹删除失败: {e}")
            return False


    javaDownload_path = None
    if system_64_bits():
        javaDownload_path = \
            "https://download.bell-sw.com/java/17.0.9+11/bellsoft-jdk17.0.9+11-windows-amd64-lite.zip"
    else:
        javaDownload_path = \
            "https://download.bell-sw.com/java/17.0.9+11/bellsoft-jdk17.0.9+11-windows-i586-lite.zip"
        print(create_terminal(""
                              "当前是32位系统，最大运行可用堆将会被限制在 1G(1024MB)，如要取消限制：\n"
                              "1.更改.MSAI里的配置文件取消限制（不建议这样做，可能会导致运行报错，可以尝试在3072之间调整）\n"
                              "2.更换为64位系统",
                              fg_color="black",
                              bg_color="red",
                              mode="underline"
                              ))

    print('JavaZip文件文件下载地址：', highlight_color(javaDownload_path))


    def file_exists(file_path):
        return os.path.exists(file_path)


    def does_the_directory_exist(dir_path, create=True):
        # 判断目录是否存在
        if os.path.exists(dir_path):
            return True  # 存在
        else:
            if create:
                # 创建目录
                os.makedirs(dir_path)
            return False  # 不存在


    does_the_directory_exist(environment_path)
    does_the_directory_exist(server_path)
    does_the_directory_exist(serverLog_path)


    def is_zipfile_complete(file_path):
        try:
            with zipfile.ZipFile(file_path) as zip_ref:
                return zip_ref.testzip() is None
        except zipfile.BadZipFile:
            return False


    def unzip_jdk(
            zip_file=javaZip_path,
            extract_path=environment_path,
            raw_folder_name='jdk-17.0.9-lite',
            new_folder_name='jdk17'
    ):
        if is_zipfile_complete(zip_file):
            with zipfile.ZipFile(zip_file, 'r') as zip_ref:
                total_files = len(zip_ref.namelist())

                with tqdm(total=total_files, desc="Extracting", unit="file") as pbar:
                    for file_index, member in enumerate(zip_ref.namelist()):
                        zip_ref.extract(member, extract_path)

                        # 更新进度条
                        progress = (file_index + 1) / total_files * 100
                        pbar.set_postfix(progress=f"{progress:.2f}%")
                        pbar.update(1)

            # 重命名文件夹
            extracted_folder = os.path.join(extract_path, raw_folder_name)
            new_folder_path = os.path.join(extract_path, new_folder_name)
            os.rename(extracted_folder, new_folder_path)
        else:
            print('不是完整的zip文件')


    def check_java_installation(java_path):
        try:
            # 执行java命令，获取java版本信息
            command = f'"{java_path}" -version'
            result_java = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            result_java.communicate()  # 等待进程执行完毕
            if result_java.returncode == 0:
                # Java安装完整，输出版本信息
                return True
            else:
                # Java未安装或安装不完整
                print(red_highlight_color("Java 未安装或安装不完整。"))
                return False
        except FileNotFoundError:
            # 找不到java命令，Java未安装或安装不完整
            print(red_highlight_color("Java 未安装或安装不完整。"))
            return False


    def verify_jar_integrity(jar_path):
        try:
            command = f'"{jarFile_path}" tf "{jar_path}"'
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            process.communicate()  # 等待进程执行完毕
            if process.returncode == 0:
                # print("命令执行成功。")
                return True
            else:
                # print("命令失败并出现错误。")
                return False
        except FileNotFoundError:
            return False


    def execute_command(command):
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True
        )

        while True:
            output = process.stdout.readline().strip()
            if output == '' and process.poll() is not None:
                break
            if output:
                print(output)

        return process.poll()


    def create_time():
        # 获取当前日期时间
        dt = datetime.datetime.now()
        # 设置目标时区
        target_timezone = pytz.timezone(str(get_localzone()))
        # 将当前日期时间转换为目标时区
        dt = dt.astimezone(target_timezone)
        # 使用 strfTime 函数将当前日期时间对象格式化为字符串
        formatted_date = dt.strftime("%a %b %d %H:%M:%S %Z %Y")
        return formatted_date


    def delete_file(file_path):
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"文件 {file_path} 删除成功")
        else:
            print(f"文件 {file_path} 不存在")


    def download_file(url, save_path):
        response = requests.get(url, stream=True)
        total_size = int(response.headers.get('content-length', 0))

        with open(save_path, 'wb') as f:
            with tqdm(total=total_size, unit='B', unit_scale=True) as pbar:
                for chunk in response.iter_content(1024):
                    if chunk:
                        f.write(chunk)
                        pbar.update(len(chunk))


    def auto_memory():  # 返回单位 字节(bytes)
        user_memory = str(user_config['最大内存']).lower()
        pure_numbers_user_memory = re.sub(r'\D', '', user_memory)
        if user_memory and pure_numbers_user_memory.isdigit():
            pure_numbers_user_memory = int(pure_numbers_user_memory)
            if re.match(r'^\d+$', user_memory):
                return pure_numbers_user_memory
            elif re.match(r'^\d+k$', user_memory):
                return pure_numbers_user_memory * 1024  # 换算bit
            elif re.match(r'^\d+m$', user_memory):
                return pure_numbers_user_memory * 1024 * 1024  # 换算bit
            elif re.match(r'^\d+g$', user_memory):
                return pure_numbers_user_memory * 1024 * 1024 * 1024  # 换算bit
            else:
                user_config['最大内存'] = ''
                print(red_highlight_color('用户配置的“最大内存”不符合规定\n已恢复默认设置'))
        print('自动配置内存')
        virtual_memory = psutil.virtual_memory()
        available_memory = virtual_memory.available
        max_memory = 1 * 1024 * 1024 * 1024  # 最大内存1G
        if system_64_bits():
            return ""
        else:
            if available_memory < max_memory:
                return available_memory
            else:
                return max_memory


    def is_the_port_occupied():
        if file_exists(serverProperties_path):
            # 读取server.properties文件
            with open(serverProperties_path, "r") as file:
                properties = file.read()

            # 使用正则表达式获取server-port的值
            port_match = re.search(r'^server-port=(\d+)', properties, flags=re.MULTILINE)
            if port_match:
                port_value = port_match.group(1)
                print("server-port 值:", port_value)

                # 判断是否为纯数字
                if port_value.isdigit():
                    port = int(port_value)

                    # 检查端口是否被占用
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    try:
                        sock.bind(("localhost", port))
                        print("端口可用：", port)
                    except socket.error as e:
                        print("端口已被使用：", e)
                        while True:
                            print(
                                '当前端口“%s”被占用，启动服务器时可能会出现错误，你可以修改端口 或者 什么都不输入按下回车Enter保持这个端口' % port)
                            new_port = input('新端口：')
                            if new_port.isspace() or new_port == '':
                                print('保持端口：', port)
                                break
                            else:
                                if new_port.isdigit():
                                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                                    try:
                                        sock.bind(("localhost", int(new_port)))

                                        with open(serverProperties_path, 'r+') as file:
                                            lines = file.readlines()

                                            # 寻找以 "server-port=" 开头的行
                                            for i, line in enumerate(lines):
                                                if line.startswith('server-port='):
                                                    # 将该行的值修改为新的值
                                                    lines[i] = 'server-port=' + new_port + '\n'

                                            # 将修改后的内容重新写入文件
                                            file.seek(0)
                                            file.writelines(lines)
                                        break

                                    except socket.error as e:
                                        print("端口“%s”已被使用：" % new_port, e)
                    finally:
                        sock.close()
                else:
                    print("服务器端口不是有效的数字。")
            else:
                print("在 server.properties 文件中找不到服务器端口。")
                with open(serverProperties_path, "a") as file:
                    file.write("\nserver-port=25565\n")
                print("在 server.properties 中写入了25565端口")
                is_the_port_occupied()
        else:
            # 打开文件并写入内容
            with open(serverProperties_path, "w") as file:
                file.write("#Minecraft server properties")
                file.write("#%s\n" % create_time())
                file.write("server-port=25565\n")
            print('创建server.properties文件完成')
            is_the_port_occupied()


    # 执行cmd命令并获取输出结果
    result = subprocess.run('cd /d "%s"' % current_path, stdout=subprocess.PIPE, shell=True, encoding='utf-8')


    def runserver():
        global run_restart
        run_restart += 1
        if run_restart >= 10:
            os.system(' start cmd.exe /K echo 啊哦！重启次数达到限制 ')
            sys.exit(0)

        if file_exists(javaZip_path) and is_zipfile_complete(javaZip_path):
            print("JavaZip文件存在，即将解压")
            unzip_jdk()
            delete_file(javaZip_path)
            runserver()
        elif file_exists(javaFile_path) and check_java_installation(javaFile_path):
            print("Java17存在")

            if java_64_bits(javaFile_path):
                if not system_64_bits():
                    delete_folder(jdkDir_path)
                    print(red_highlight_color('当前系统为64位，但是Java是32位，即将删除重新下载'))
                    runserver()
                    return
            else:
                if system_64_bits():
                    delete_folder(jdkDir_path)
                    print(red_highlight_color('当前系统为32位，但是Java是64位，即将删除重新下载'))
                    runserver()
                    return

            if file_exists(serverFile_path):
                print("服务器文件存在，即将运行")
                if verify_jar_integrity(serverFile_path):
                    if not file_exists(eulaFile_path):
                        # 打开文件并写入内容
                        with open(eulaFile_path, "w") as file:
                            file.write(
                                "#By changing the setting below to TRUE you are indicating "
                                "your agreement to our EULA "
                                "(https://aka.ms/MinecraftEULA).\n"
                            )
                            file.write("#%s\n" % create_time())
                            file.write("eula=true\n")
                        print('创建eula文件完成')
                    is_the_port_occupied()
                    # 运行命令
                    allocate_memory = auto_memory()
                    allocate_memory_xmx = ''
                    if allocate_memory != '':
                        allocate_memory_xmx = f' -Xmx{allocate_memory}'
                    command = f'"{javaFile_path}"{allocate_memory_xmx} -jar "{serverFile_path}" nogui'
                    print('服务器运行命令：', highlight_color(command))
                    # 构建完整的命令字符串
                    complete_startup_command = f'''  cd /d "{server_path}" && {command}  '''
                    print('完整启动命令', highlight_color(complete_startup_command))

                    if allocate_memory == '':
                        allocate_memory_str = "Java自适应"
                    else:
                        allocate_memory_str = str(allocate_memory / 1024 / 1024) + 'MB'

                    print(green_highlight_color(
                        "\n"
                        f'您的服务器开启成功！！\n'
                        f'为您分配了内存 {allocate_memory_str}\n'
                        f'如要停止您的服务器，请在控制台输入“stop”'
                        "\n"
                    ))
                    os.system(complete_startup_command)
                else:
                    print(red_highlight_color('服务器文件损坏，即将重新下载'))
                    delete_file(serverFile_path)
                    download_file(paperServerFile_path, serverFile_path)
                    runserver()
            else:
                print(red_highlight_color('服务器文件不存在，即将下载'))
                download_file(paperServerFile_path, serverFile_path)
                print("下载完成，即将运行")
                runserver()
        else:
            delete_folder(jdkDir_path)
            print(red_highlight_color('不存在Java17或Java17压缩包，即将下载'))
            download_file(javaDownload_path, javaZip_path)
            print("下载Java17压缩包完成，即将解压")
            unzip_jdk()
            print("解压完成")
            delete_file(javaZip_path)
            runserver()


    # 调用函数判断文件是否存在
    runserver()

except KeyboardInterrupt:
    # 在捕获到KeyboardInterrupt异常时执行的操作
    print("程序终止")
    exit(0)

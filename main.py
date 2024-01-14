# <a target="_blank" href="https://icons8.com/icon/XfjNd4vkhBBy/minecraft-grass-cube">Minecraft</a>
# 图标来自
# <a target="_blank" href="https://icons8.com">Icons8</a>
import os
import subprocess
import sys
import time

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
from color import create_terminal
import psutil

try:
    def highlight_color(data):
        return create_terminal(data=data, fg_color="黄色", bg_color="黑色", mode="加粗")


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
    javaDownload_path = \
        "https://download.bell-sw.com/java/17.0.9+11/bellsoft-jdk17.0.9+11-windows-i586-full.zip"
    # "https://download.bell-sw.com/java/17.0.9+11/bellsoft-jdk17.0.9+11-windows-i586.zip"

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
            raw_folder_name='jdk-17.0.9',
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


    def verify_jar_integrity(jar_path):
        command = "\"%s\" tf \"%s\"" % (jarFile_path, jar_path)
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        stdout, stderr = process.communicate()

        if process.returncode == 0:
            # print("命令执行成功。")
            return True
        else:
            # print("命令失败并出现错误。")
            return False


    def show_message_box(message, title):
        def show_message_box_():
            win32api.MessageBox(0, message, title, win32con.MB_ICONINFORMATION)

        message_thread = threading.Thread(target=show_message_box_)
        message_thread.start()


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
        virtual_memory = psutil.virtual_memory()
        available_memory = virtual_memory.available
        max_memory = 4 * 1024 * 1024 * 1024  # 最大内存4G
        if available_memory < max_memory:
            return available_memory - 10000
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
        else:
            if file_exists(javaFile_path):
                print("Java17存在")

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
                        command = f'""{javaFile_path}"" -Xmx{auto_memory()} -jar ""{serverFile_path}"" nogui'
                        print('服务器运行命令：', highlight_color(command))
                        # 构建完整的命令字符串
                        complete_startup_command = 'start cmd /K "cd /d ""%s"" && %s"' % (server_path, command)
                        os.system(complete_startup_command)
                        print('完整启动命令', highlight_color(complete_startup_command))

                        show_message_box('您的服务器开启成功！！\n如要停止您的服务器，请在控制台输入“stop”', '')

                        print('服务器启动成功！')
                    else:
                        print('服务器文件损坏，即将重新下载')
                        delete_file(serverFile_path)
                        download_file(paperServerFile_path, serverFile_path)
                        runserver()
                else:
                    print("服务器文件不存在，即将下载")
                    download_file(paperServerFile_path, serverFile_path)
                    print("下载完成，即将运行")
                    runserver()
            else:
                print("不存在Java17或Java17压缩包，即将下载")
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
    sys.exit(0)

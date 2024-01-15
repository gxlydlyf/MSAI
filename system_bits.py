import platform
import subprocess


def system_64_bits():
    machine = platform.machine()
    # print(machine)
    if machine.endswith('64'):
        # print("64位Windows操作系统")
        return True
    else:
        # print("32位Windows操作系统")
        return False


def java_64_bits(java_path):
    output = subprocess.check_output(f'"{java_path}" -version', stderr=subprocess.STDOUT, shell=True)
    java_info = output.decode('utf-8')
    if '64-Bit' in java_info:
        # print("64位Java运行环境")
        return True
    else:
        # print("32位Java运行环境")
        return False

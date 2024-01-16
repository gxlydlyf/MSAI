import os
import re
# import traceback
from collections import OrderedDict


class SimpleConfiguration:
    def __init__(self, default_config, absolute_path='', file_name='config.txt'):
        # print(default_config)
        self.__current_file_dir = os.path.dirname(os.path.abspath(__file__))
        if self.__isspace(absolute_path):
            absolute_path = self.__current_file_dir
        if not isinstance(absolute_path, str):
            raise ValueError("绝对路径必须是字符串")
        if not isinstance(file_name, str):
            raise ValueError("配置文件名必须是字符串")
        if not isinstance(default_config, dict):
            raise ValueError("默认配置必须是字典")
        default_config = self.__process_dict(default_config)
        self.__raw_default_config = default_config
        self.__default_config = {key: value for key, value in default_config.items() if not key.startswith("#")}
        if self.__isspace(self.__default_config):
            raise ValueError("默认配置不能为空", self.__default_config)
        self.__file_name = file_name
        self.__absolute_path = absolute_path
        self.__config_file_path = f"{self.__absolute_path}/{self.__file_name}"
        self.__check_and_get_file_config()

    def __setitem__(self, key, value):
        if not (key in self.__default_config):
            raise PermissionError("禁止添加键")
        self.__check_and_get_file_config(update_key=key, update_value=value)

    def __getitem__(self, key):
        if not (key in self.__default_config):
            raise KeyError(f"键“{key}”不存在")
        return self()[key]

    def __delitem__(self, key):
        raise PermissionError("禁止删除键")

    def __repr__(self):
        return str(self())

    def __str__(self):
        return str(self())

    def __len__(self):
        return len(self())

    def __contains__(self, item):
        return item in self.__default_config

    def __iter__(self):
        return iter(self())

    def __getattr__(self, item):
        return self[item]

    def __call__(self, *args, **kwargs):
        return self.__check_and_get_file_config()

    def items(self):
        return self().items()

    def __check_and_get_file_config(self, update_key='', update_value=''):
        file_config = {}
        self.__create_directory_if_not_exists(self.__absolute_path)
        self.__create_file_if_not_exists(self.__config_file_path)
        with open(file=self.__config_file_path, mode="r+", encoding='utf-8') as file:
            lines = file.readlines()  # 读取所有行
            if self.__isspace(lines):  # 空文件
                # 将修改后的内容写回文件
                file.seek(0)  # 将文件指针移动到文件开头
                file.write(self.__create_default_config_text())
                file.truncate()  # 清空文件从当前位置之后的内容
            file.seek(0)
            lines = file.readlines()  # 读取所有行

            for i in range(len(lines)):
                # print(lines[i])

                if lines[i].startswith("# "):
                    # 字符串以 '# ' 开头
                    continue
                elif lines[i].startswith("#"):
                    # 字符串以 '#' 开头，进行替换
                    lines[i] = lines[i].replace("#", "# ", 1)
                elif self.__isspace(lines[i]):  # 空行
                    continue
                else:
                    # "字符串不以 '#' 开头
                    lines[i] = lines[i].strip() + '\n'
                    if self.__content_replace_pattern(lines[i]) is None:  # 没有匹配到“=”
                        lines[i] = '# ' + lines[i]
                        continue
                    else:
                        lines[i] = self.__content_replace_pattern(lines[i])
                    line_match = re.search(r'(.*) = (.*)', lines[i])
                    line_key = line_match.group(1)
                    line_value = line_match.group(2)
                    # print(line_key)
                    if line_key not in self.__default_config:
                        lines[i] = '# ' + lines[i]  # 没包含在默认配置里的键替换为注释
                        continue
                    if line_key in file_config:
                        lines[i] = '# ' + lines[i]  # 重复的键
                        continue
                    if self.__is_string_enclosed(line_value) is False:
                        lines[i] = f"{line_key} = \"{line_value}\"\n"  # 给字符串包上“"”
                        line_value = f"\"{line_value}\""

                    line_quote_character = self.__get_string_enclosed(line_value)

                    if update_key == line_key:
                        line_value = f"{line_quote_character}{update_value}{line_quote_character}"
                        lines[i] = f"{line_key} = {line_value}\n"
                    file_config[line_key] = self.__is_string_enclosed(line_value)

            if lines:  # 列表非空
                if not lines[-1].endswith("\n"):
                    lines[-1] = lines[-1] + '\n'  # 如果最后一项不是\n(换行符)结尾就替换

            for key, value in self.__default_config.items():
                if not (key in file_config):
                    key_index = self.__get_key_index(dictionary=self.__default_config, key=key)
                    if f"#{key_index + 1}" \
                            in self.__raw_default_config:  # 补充注释
                        last_non_empty_line = self.__get_last_non_empty_item(lines)
                        line_exegesis = f"# {self.__raw_default_config[f'#{key_index + 1}']}\n"
                        if last_non_empty_line is not None:
                            if last_non_empty_line != line_exegesis:
                                lines.append(line_exegesis)
                    if update_key == key:
                        lines.append(f"{key} = \"{update_value}\"\n")
                        file_config[key] = update_value
                    else:
                        lines.append(f"{key} = \"{value}\"\n")
                        file_config[key] = value

            # 将修改后的内容写回文件
            file.seek(0)  # 将文件指针移动到文件开头
            file.writelines(lines)
            file.truncate()  # 清空文件从当前位置之后的内容

        return file_config

    def __create_default_config_text(self):
        dc = self.__raw_default_config
        text_config = ''
        for key, value in dc.items():
            if key.startswith("#"):
                text_config += f"# {value}\n"
            else:
                text_config += f"{key} = \"{value}\"\n"
        # print(text_config)
        return text_config

    @staticmethod
    def __process_dict(dictionary):
        new_dict = {}
        for key, value in dictionary.items():
            if isinstance(key, (int, float, str)) and isinstance(value, (int, float, str)):
                new_dict[str(key)] = str(value)
            else:
                raise ValueError("字典中的键和值必须为数字或字符串类型")

        dictionary.clear()
        dictionary.update(new_dict)
        return dictionary

    @staticmethod
    def __content_replace_pattern(string, replacement=' = '):
        pattern = rf'\s*=\s*'

        match = re.search(pattern, string)
        if match:
            new_text = re.sub(pattern, replacement, string, count=1)
            return new_text

        return None

    @staticmethod
    def __is_string_enclosed(string):
        if (string.startswith('\"') and string.endswith('\"')) or \
                (string.startswith('\'') and string.endswith('\'')) or \
                (string.startswith('`') and string.endswith('`')):
            return string[1:-1]
        else:
            return False

    @staticmethod
    def __get_string_enclosed(string):
        if string.startswith('\"') and string.endswith('\"'):
            return "\""
        elif string.startswith('\'') and string.endswith('\''):
            return "\'"
        elif string.startswith('`') and string.endswith('`'):
            return '`'
        else:
            return None

    @staticmethod
    def __get_key_index(dictionary, key):
        keys_list = list(dictionary.keys())
        if key in keys_list:
            index = keys_list.index(key)
            return index
        else:
            return None

    @staticmethod
    def __create_directory_if_not_exists(dir_path, create=True):
        # 判断目录是否存在
        if os.path.exists(dir_path):
            return True  # 存在
        else:
            if create:
                # 创建目录
                os.makedirs(dir_path)
            return False  # 不存在

    @staticmethod
    def __create_file_if_not_exists(file_path, create=True):
        exist = os.path.exists(file_path)
        if exist:
            return True
        else:
            if create is True:
                open(file_path, 'w').close()
            return False

    def __get_last_non_empty_item(self, collection):
        if isinstance(collection, dict):  # 如果是字典
            ordered_dict = OrderedDict(collection)
            while ordered_dict:
                key, value = ordered_dict.popitem(last=True)
                if not self.__isspace(key, value):
                    return key, value
        elif isinstance(collection, (list, tuple)):  # 如果是列表或元组
            lst = list(collection)
            while lst:
                item = lst.pop()
                if not self.__isspace(item):
                    return item
        return None

    def __isspace(self, *variables):  # 是否为空
        for variable in variables:
            if (variable is None) or (variable == "") or (variable == []) or \
                    (variable == {}) or (variable == set()) or (variable == ()):
                return True
            elif isinstance(variable, (list, tuple)):
                for value in variable:
                    value = value.strip()
                    if not (value == "" or self.__isspace(value)):
                        return False
            elif isinstance(variable, str):
                variable = variable.strip()
                if not (variable == "" or variable.isspace()):
                    return False
            elif isinstance(variable, dict):
                for key in variable:
                    if not self.__isspace(key):
                        return False
        return True


if __name__ == "__main__":
    # 在这里执行作为主程序时的命令或代码块
    sc = SimpleConfiguration(
        absolute_path=os.getcwd(),
        default_config={
            "#1": "设置",
            "setting": "3",
            "#2": "最大",
            "max": "2",
            "#3": "最小",
            "small": "1",
            "#4": "大",
            "big": "4",
            "非常的大": "big",
            'config': "ss",
            'items': "ss"
        },
        file_name='testConfig.txt'
    )
    print("sc:", type(sc))
    print("sc():", type(sc()))

    print('')

    sc['big'] = '222'
    print('big', sc['big'])
    try:
        sc['sma'] = 'dd'
    except PermissionError:
        # traceback.print_exc()
        print('PermissionError,dd')
    try:
        del sc['sma']
    except PermissionError:
        # traceback.print_exc()
        print('PermissionError,sma')
    print("big", sc.big)
    print("非常的大", sc.非常的大)
    print("config", sc.config)
    print("sc['items']", sc['items'])
    print("sc.items", sc.items)

    print('')

    if 'big' in sc:
        print('big in')
    if 'very big' not in sc:
        print('very big not in')

    print('')

    for key2, value2 in sc.items():
        print(f"{key2} = {value2}")
    for kv in sc:
        print(kv)

    print('')

    print("str:", str(sc))
    print("repr:", repr(sc))
    print("object:", sc)

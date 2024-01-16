class ConfigManager:
    def __init__(self, default_config):
        self.default_config = default_config
        self.config = {}
        self.comments = []

    def read_config(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                for line in file:
                    line = line.strip()
                    if line.startswith('#'):
                        self.comments.append(line)
                        continue

                    if '=' in line:
                        key, value = line.split('=')
                        self.config[key.strip()] = value.strip()
                    else:
                        self.comments.append('# ' + line)

        except FileNotFoundError:
            self.config = self.default_config

    def write_config(self, file_path):
        with open(file_path, 'w', encoding='utf-8') as file:
            for comment in self.comments:
                file.write(f"{comment}\n")

            for key, value in self.config.items():
                file.write(f"{key} = {value}\n")

    def update_config(self, key, value):
        self.config[key] = value


# 示例使用方法：
default_config = {
    'key1': 'value1',
    'key2': 'value2',
}

config_manager = ConfigManager(default_config)
config_manager.read_config('config.txt')

print(config_manager.config)

config_manager.update_config('key1', 'new_value')
config_manager.update_config('key3', 'value3')

config_manager.write_config('config.txt')
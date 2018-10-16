import os
import yaml

class Config:
    CONFIG_DIR = os.path.join(os.getcwd(), ".releasy")
    CONFIG_FILE = os.path.join(CONFIG_DIR, "config.yml")
    ISSUES_FILE = os.path.join(CONFIG_DIR, "issues.yml")

    def __init__(self):
        self.__config = {}
        self.__read_config()

    def __read_config(self):
        print(os.path.dirname(Config.CONFIG_FILE))
        if not os.path.isdir(Config.CONFIG_DIR):
            os.mkdir(Config.CONFIG_DIR)
        if os.path.exists(Config.CONFIG_FILE):
            with open(Config.CONFIG_FILE, 'r') as stream:
                try:
                    self.__config = yaml.load(stream)
                except yaml.YAMLError as exc:
                    print(exc)
                    raise

    def __write_config(self):
        with open(Config.CONFIG_FILE, 'w') as config_file:
            yaml.dump(self.__config, config_file, default_flow_style=False)

    @property
    def prop(self):
        return self.__config

    def isnew(self):
        if not self.__config:
            return True
        else:
            return False

    def save(self):
        self.__write_config()
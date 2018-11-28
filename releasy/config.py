import os
import yaml

class Config:
    def __init__(self, base_dir=None):
        self.__config = {}
        base_dir = base_dir if base_dir else os.getcwd()
        self.base_dir = os.path.join(base_dir, ".releasy")
        self.config_file = os.path.join(self.base_dir, "config.yml")
        self.issues_file = os.path.join(self.base_dir, "issues.json")
        self.__read_config()

    def __read_config(self):
        if not os.path.isdir(self.base_dir):
            os.mkdir(self.base_dir)
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as stream:
                try:
                    self.__config = yaml.load(stream)
                except yaml.YAMLError as exc:
                    print(exc)
                    raise

    def __write_config(self):
        with open(self.config_file, 'w') as config_file:
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
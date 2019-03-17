

class BaseCli:
    """ Base class for Cli """
    def __init__(self):
        self.help=None
        self.args=None

    def build_parser(self, parser):
        pass

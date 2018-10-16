
class Cmd:
    def __init__(self, config=None):
        self.config = config

class Project_Cmd(Cmd):
    def __init__(self, config=None):
        super().__init__(config)
        self.project = None

    def require_project(self):
        return True


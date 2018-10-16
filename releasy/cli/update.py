from releasy.cli.base import Cmd

class Update():
    def __init__(self, user, ask_password=True):
        self.user = user
        self.ask_password=ask_password

    def run(self):
        

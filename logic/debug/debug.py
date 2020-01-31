class Debug:

    MATH = 1

    def __init__(self):
        self.active = False

    def log(self, msg, category):
        if self.active:
            print(msg)
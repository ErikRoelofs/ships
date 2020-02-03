class Debug:

    COMBAT = 2
    MATH = 1

    def __init__(self):
        self.active = True

    def log(self, msg, category):
        if self.active:
            print(msg)

    def is_active(self) -> bool:
        return self.active

class Debug:

    COMBAT = 2
    MATH = 1
    SHIP_STATUS = 3

    def __init__(self):
        self.active = False
        self.active_categories = [Debug.COMBAT]

    def log(self, msg, category):
        if self.active and category in self.active_categories:
            print(msg)

    def is_active(self) -> bool:
        return self.active

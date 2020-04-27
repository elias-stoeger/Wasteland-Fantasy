class Enemy:
    def __init__(self):
        self.tier = self.tier()
        self.type_ = self.enemy()

    def enemy(self):
        return "Hey there!"

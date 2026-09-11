class Score:
    def __init__(self):
        self.value = 0

    def increment(self, amount=1):
        self.value += amount

    def reset(self):
        self.value = 0

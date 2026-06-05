class Score:

    def __init__(self):
        self.points = 0

    def add(self, value):
        self.points += value

    def subtract(self, value):
        self.points = max(0, self.points - value)

    def reset(self):
        self.points = 0

    def is_zero(self):
        return self.points <= 0

    def __int__(self):
        return self.points

    def __str__(self):
        return str(self.points)

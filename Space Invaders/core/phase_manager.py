class PhaseManager:

    THRESHOLDS = [
        (300, 4),
        (200, 3),
        (100, 2),
        (0,   1),
    ]

    def __init__(self):
        self.phase = 1

    def update(self, score):
        for min_score, phase in self.THRESHOLDS:
            if score >= min_score:
                self.phase = phase
                return

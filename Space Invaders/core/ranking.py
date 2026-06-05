import json
import os
from datetime import datetime


RANKING_FILE = "ranking.json"
MAX_ENTRIES = 10


class Ranking:

    def __init__(self, filepath=RANKING_FILE):
        self.filepath = filepath
        if not os.path.exists(self.filepath):
            self._save([])

    def _load(self):
        with open(self.filepath, "r") as f:
            return json.load(f)

    def _save(self, data):
        with open(self.filepath, "w") as f:
            json.dump(data, f, indent=2)

    def add_score(self, name, score):
        ranking = self._load()
        ranking.append({
            "name": name,
            "score": int(score),
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        })
        ranking = sorted(ranking, key=lambda x: x["score"], reverse=True)[:MAX_ENTRIES]
        self._save(ranking)

    def get_top(self):
        return self._load()

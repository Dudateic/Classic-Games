import json, os
from config.settings import SCORE_TABLE, LEVEL_LINES, BASE_FALL_TICKS, MAX_SCORES

SCORES_FILE = os.path.join(os.path.dirname(__file__), '..', 'scores.json')

class Scorer:

    def __init__(self):
        self.score  = 0.0
        self.lines  = 0
        self.level  = 1
        self.combo  = 0   # consecutivas com linhas

    def add_lines(self, count: int) -> float:
        if count == 0:
            self.combo = 0
            return 0.0
        base    = SCORE_TABLE.get(count, count * 200)
        combo_b = 50 * self.combo * self.level
        gained  = (base + combo_b) * self.level
        self.score  += gained
        self.lines  += count
        self.level   = (self.lines // LEVEL_LINES) + 1
        self.combo  += 1
        return gained

    def get_current_fall_ticks(self) -> int:
        return max(4, BASE_FALL_TICKS - (self.level - 1) * 4)


def load_scores() -> list[dict]:
    try:
        with open(SCORES_FILE, 'r') as f:
            data = json.load(f)
        return sorted(data, key=lambda x: x['score'], reverse=True)[:MAX_SCORES]
    except Exception:
        return []

def save_score(name: str, score: int, lines: int, level: int) -> tuple[list[dict], int]:
    """Salva pontuação e retorna (lista atualizada, posição alcançada 1-based)."""
    scores = load_scores()
    entry  = {'name': name.upper()[:12], 'score': score, 'lines': lines, 'level': level}
    scores.append(entry)
    scores = sorted(scores, key=lambda x: x['score'], reverse=True)[:MAX_SCORES]
    try:
        with open(SCORES_FILE, 'w') as f:
            json.dump(scores, f)
    except Exception:
        pass
    pos = next((i+1 for i, e in enumerate(scores) if e is entry or
                (e['name']==entry['name'] and e['score']==entry['score'])), MAX_SCORES)
    return scores, pos

def get_first_place_score() -> int:
    scores = load_scores()
    return scores[0]['score'] if scores else 0

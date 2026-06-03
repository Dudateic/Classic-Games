import pathlib
import json
from typing import List, Dict

_SCORE_FILE = pathlib.Path.home() / ".breakout_scores"
MAX_ENTRIES = 5


def load_scores() -> List[Dict]:
    """Retorna lista de até MAX_ENTRIES dicts: {name, score, level}."""
    try:
        data = json.loads(_SCORE_FILE.read_text())
        if isinstance(data, list):
            return data[:MAX_ENTRIES]
    except (FileNotFoundError, ValueError, json.JSONDecodeError):
        pass
    return []


def save_scores(scores: List[Dict]) -> None:
    try:
        _SCORE_FILE.write_text(json.dumps(scores[:MAX_ENTRIES]))
    except OSError:
        pass


def add_score(score: int, level: int, name: str = "---") -> List[Dict]:
    """Insere nova pontuação, ordena e salva. Retorna lista atualizada."""
    scores = load_scores()
    scores.append({"name": name, "score": score, "level": level})
    scores.sort(key=lambda x: x["score"], reverse=True)
    scores = scores[:MAX_ENTRIES]
    save_scores(scores)
    return scores


def load_high_score() -> int:
    """Compatibilidade – retorna apenas o maior valor."""
    scores = load_scores()
    if scores:
        return scores[0]["score"]
    return 0


def save_high_score(score: int) -> None:
    """Compatibilidade – adiciona com nome padrão."""
    add_score(score, 1)

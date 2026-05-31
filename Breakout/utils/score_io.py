import pathlib

_SCORE_FILE = pathlib.Path.home() / ".breakout_highscore"


def load_high_score() -> int:
    try:
        return int(_SCORE_FILE.read_text().strip())
    except (FileNotFoundError, ValueError):
        return 0


def save_high_score(score: int) -> None:
    try:
        _SCORE_FILE.write_text(str(score))
    except OSError:
        pass

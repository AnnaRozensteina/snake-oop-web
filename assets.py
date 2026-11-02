from pathlib import Path
import sys

def asset_path(filename):
    if getattr(sys, "frozen", False):
        base_path = Path(sys._MEIPASS)
    else:
        base_path = Path(__file__).parent

    return base_path / "assets" / filename
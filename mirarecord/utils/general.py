import os
from pathlib import Path


def get_asset_path():
    current_file_dir = Path(__file__).parent
    path = (current_file_dir / '../../assets').resolve()
    return str(path)
import os
from .general import get_asset_path


class ImageUtils:
    @staticmethod
    def asset(path: str):
        return os.path.join(get_asset_path(), path)
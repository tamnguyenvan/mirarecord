from typing import Dict, List
from dataclasses import dataclass


@dataclass
class EditorState:
    input_path: str = ''
    is_video_playing: bool = False
    mouse_history: Dict[str, List[int]] = None
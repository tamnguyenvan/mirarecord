from dataclasses import dataclass


@dataclass
class EditorState:
    input_path: str = ''
    is_video_playing: bool = False
from abc import ABC

class EditorEvent(ABC):
    pass


class EditorInitSet(EditorEvent):
    pass


class EditorPlayVideoSet(EditorEvent):
    pass


class EditorPauseVideoSet(EditorEvent):
    pass


class EditorNextVideoSet(EditorEvent):
    pass


class EditorPreviousVideoSet(EditorEvent):
    pass
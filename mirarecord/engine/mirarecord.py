import time
import os
import threading
from typing import List
from abc import ABC, abstractmethod
from dataclasses import dataclass

import cv2
import numpy as np
from loguru import logger
from vidgear.gears import ScreenGear
from pynput.mouse import Listener
from PyQt6.QtGui import QImage

from mirarecord.utils.file import generate_filename


class Engine(ABC):
    pass


class MiraRecorder(Engine):
    def __init__(
        self,
        root_dir: str = '~/.mirarecord',
        record_mouse: bool = True,
    ):
        super().__init__()
        self.root_dir = os.path.expanduser(root_dir)
        if not os.path.exists(self.root_dir):
            os.makedirs(self.root_dir, exist_ok=True)

        self.video_path = self._generate_video_path(self.root_dir)

        # Backend recorder
        self.stream = ScreenGear().start()
        self.record_thread = None
        self.mouse_listener_thread = None

        # State and params
        self.is_stopped = threading.Event()
        self.max_error_frames = 100

    def _generate_video_path(self, root_dir):
        filename = generate_filename(extension='.mp4')
        return os.path.join(root_dir, filename)

    def _record(self):
        logger.info('Recording')
        logger.info('Video path', self.video_path)
        self.is_stopped.clear()
        error_frames_count = 0

        writer = None
        frame_idx = 0
        while not self.is_stopped.is_set():
            frame = self.stream.read()
            if frame is None:
                time.sleep(0.1)
                error_frames_count += 1
                if error_frames_count >= self.max_error_frames:
                    break
                else:
                    continue

            frame_idx += 1
            error_frames_count = 0
            if writer is None:
                frame_h, frame_w = frame.shape[:2]
                writer = cv2.VideoWriter(self.video_path, cv2.VideoWriter_fourcc(*'mp4v'), 30, (frame_w, frame_h))

            if writer is not None:
                writer.write(frame)

        if writer is not None:
            logger.info(f'Saved output video as: {self.video_path}')
            writer.release()
        self.stream.stop()

    def _on_mouse_listener(self):
        def on_move(x, y):
            # print('Pointer moved to {0}'.format((x, y)))
            pass

        def on_click(x, y, button, pressed):
            # print('{0} at {1}'.format(
            #     'Pressed' if pressed else 'Released', (x, y)))
            pass

        def on_scroll(x, y, dx, dy):
            # print('Scrolled {0} at {1}'.format(
            #     'down' if dy < 0 else 'up', (x, y)))
            pass

        logger.info('Mouse listener started')
        with Listener(
            on_move=on_move,
            on_click=on_click,
            on_scroll=on_scroll
        ):
            while True:
                self.is_stopped.wait()
                if self.is_stopped.is_set():
                    logger.info('Mouse listener stopped')
                    return

                time.sleep(0.1)

    def record(self):
        if not self.record_thread or not self.record_thread.is_alive():
            self.record_thread = threading.Thread(target=self._record)
            self.record_thread.start()

        if not self.mouse_listener_thread or not self.mouse_listener_thread.is_alive():
            self.mouse_listener_thread = threading.Thread(
                target=self._on_mouse_listener
            )
            self.mouse_listener_thread.start()

    def stop(self):
        self.is_stopped.set()
        return self.video_path

    def clean(self):
        if os.path.exists(self.video_path):
            os.remove(self.video_path)
        logger.info('Cleaned video')


class Processor(ABC):
    def apply(self):
        raise NotImplemented


class ZoomProcessor(Processor):
    def __init__(self) -> None:
        super().__init__()

    def _zoom(self):
        pass

    def apply(self):
        pass


@dataclass
class MouseFocusData:
    pass


class MouseFocusProcessor(Processor):
    def __init__(self) -> None:
        super().__init__()

    def apply(self):
        pass


@dataclass
class CutData:
    offset: float


class CutProcessor(Processor):
    def __init__(self) -> None:
        super().__init__()

    def apply(self):
        pass


@dataclass
class SpeedData:
    speed: float


class SpeedProcessor(Processor):
    def __init__(self) -> None:
        super().__init__()

    def apply(self):
        pass


@dataclass
class PaddingData:
    pad: int = 20


class PaddingProcessor(Processor):
    def __init__(self, data: PaddingData = PaddingData()) -> None:
        super().__init__()
        self.data = data

    def apply(self, frame):
        frame_height, frame_width = frame.shape[:2]
        ratio = frame_width / frame_height

        background = cv2.imread('/home/tamnv/Projects/exp/mirarecord/assets/background/background-0.jpg')

        # center crop background to fit frame size
        bh, bw = background.shape[:2]
        frame_half_w, frame_half_h = frame_width // 2, frame_height // 2
        x1, y1 = bw // 2 - frame_half_w, bh // 2 - frame_half_h
        x2, y2 = x1 + frame_width, y1 + frame_height
        cropped_background = background[y1:y2, x1:x2, :]

        pad_y = self.data.pad
        pad_x = int(pad_y * ratio)
        new_height = max(0, frame_height - 2 * pad_y)
        new_width = max(0, frame_width - 2 * pad_x)

        resized_frame = cv2.resize(frame, (new_width, new_height))
        cropped_background[pad_y:pad_y+new_height, pad_x:pad_x+new_width, :] = resized_frame
        return cropped_background


@dataclass
class VideoProcessorData:
    pass


class VideoProcessor(Processor):
    def __init__(self, video_path: str):
        super().__init__()
        self.video_path = video_path
        print('video path', video_path)
        self.processors = self._build_processors()
        self.processors = [PaddingProcessor()]

        self.video_capture = cv2.VideoCapture(self.video_path)
        self.frame_height = 0
        self.frame_width = 0

    def get(self, frame_index: int = None):
        if isinstance(frame_index, int):
            self.video_capture.set(cv2.CAP_PROP_POS_FRAMES, frame_index)

        ret, frame = self.video_capture.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_height, frame_width = frame.shape[:2]
            processed_frame = self.apply(frame)

            image = QImage(processed_frame, frame_width, frame_height, QImage.Format.Format_RGB888)
            return image

    def _build_processors(self) -> List[Processor]:
        pass

    def apply(self, frame):
        for processor in self.processors:
            frame = processor.apply(frame)
        return frame

    def save(self):
        pass

    def export(self):
        pass

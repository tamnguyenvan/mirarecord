import time
import os
import threading
from typing import Dict, List, Tuple
from abc import ABC, abstractmethod
from dataclasses import dataclass

import cv2
import numpy as np
from loguru import logger
from vidgear.gears import ScreenGear
from pynput.mouse import Listener
from PyQt6.QtGui import QImage

from mirarecord.utils.file import generate_filename
from mirarecord.utils.image import ImageUtils


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
        self.stream = ScreenGear(with_cursor=True).start()
        self.record_thread = None
        self.mouse_listener_thread = None
        self.mouse_history = {'clicks': [], 'move': []}

        # State and params
        self.is_stopped = threading.Event()
        self.max_error_frames = 100
        self.frame_index = 0

    def _generate_video_path(self, root_dir):
        filename = generate_filename(extension='.mp4')
        return os.path.join(root_dir, filename)

    def _record(self):
        logger.info('Recording')
        logger.info('Video path', self.video_path)
        self.is_stopped.clear()
        error_frames_count = 0

        writer = None
        while not self.is_stopped.is_set():
            frame = self.stream.read()
            if frame is None:
                time.sleep(0.1)
                error_frames_count += 1
                if error_frames_count >= self.max_error_frames:
                    break
                else:
                    continue

            self.frame_index += 1
            error_frames_count = 0
            if writer is None:
                frame_h, frame_w = frame.shape[:2]
                writer = cv2.VideoWriter(self.video_path, cv2.VideoWriter_fourcc(
                    *'mp4v'), 30, (frame_w, frame_h))

            if writer is not None:
                writer.write(frame)

        if writer is not None:
            logger.info(f'Saved output video as: {self.video_path}')
            writer.release()
        self.stream.stop()

    def _on_mouse_listener(self):
        def on_move(x, y):
            # print('Pointer moved to {0}'.format((x, y)))
            self.mouse_history['move'].append((x, y, self.frame_index))

        def on_click(x, y, button, pressed):
            # print('{0} at {1}'.format(
            #     'Pressed' if pressed else 'Released', (x, y)))
            self.mouse_history['clicks'].append((x, y, self.frame_index))

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
    def apply(self, frame, frame_index: int = None):
        raise NotImplemented


# Easing function for smooth zooming
def ease_in_out_quad(t):
    return t*t*(3 - 2*t) if t < 0.5 else 1 - (t-0.5)*(t-0.5)*2

# Function to calculate zoom parameters
def calculate_zoom_parameters(width, height, zoom_center, base_zoom_factor, start_time, duration, timestamp):
    # Calculate elapsed time since the start of zoom
    elapsed_time = timestamp - start_time

    # Calculate the progress of zooming from 0 to 1
    progress = min(elapsed_time / duration, 1.0)

    # Apply easing function to smooth the progress
    progress = ease_in_out_quad(progress)

    if progress <= 0.5:
        # Zoom in during the first half
        current_factor = 1.0 + (base_zoom_factor - 1.0) * (2 * progress)
    else:
        # Zoom out during the second half
        current_factor = base_zoom_factor - \
            (base_zoom_factor - 1.0) * (2 * (progress - 0.5))

    # Calculate the zoomed width and height
    zoomed_width = int(width / current_factor)
    zoomed_height = int(height / current_factor)

    # Calculate the crop region around the zoom center
    x = max(0, zoom_center[0] - zoomed_width // 2)
    y = max(0, zoom_center[1] - zoomed_height // 2)

    return current_factor, (x, y, zoomed_width, zoomed_height)


@dataclass
class ZoomData:
    interval: Tuple[float] = None
    zoom_factor: float = 2
    zoom_center: Tuple[int] = None

def find_interval(intervals, num):
    low = 0
    high = len(intervals) - 1

    while low <= high:
        mid = (low + high) // 2
        if intervals[mid][0] <= num <= intervals[mid][1]:
            return mid  # Trả về chỉ số của khoảng chứa số
        elif intervals[mid][0] > num:
            high = mid - 1
        else:
            low = mid + 1

    return -1

class ZoomProcessor(Processor):
    def __init__(self, data: List[ZoomData] = [], frame_rate: int = None) -> None:
        super().__init__()
        self.data = data
        self.intervals = [item.interval for item in data]
        self.frame_rate = frame_rate
        self.data_index = 0

    def apply(self, frame, frame_index: int = None):
        timestamp = frame_index * self.frame_rate * 0.001
        self.data_index = find_interval(self.intervals, frame_index)

        if len(self.data):
            height, width = frame.shape[:2]

            item = self.data[self.data_index]
            if item.interval[0] < frame_index < item.interval[1]:
                zoom_center = item.zoom_center
                base_zoom_factor = item.zoom_factor
                start_time = item.interval[0] * self.frame_rate * 0.001
                duration = (
                    item.interval[1] - item.interval[0]) * self.frame_rate * 0.001

                zoom_factor, crop_params = calculate_zoom_parameters(
                    width, height, zoom_center,
                    base_zoom_factor, start_time, duration, timestamp)
            else:
                zoom_factor = 1.0  # No zoom effect before the start time
                crop_params = (0, 0, width, height)  # Full frame

            # if frame_index > item.interval[1]:
            #     self.data_index = min(self.data_index + 1, len(self.data) - 1)

            # Crop the zoomed region
            x, y, zoomed_width, zoomed_height = crop_params
            zoomed_region = frame[y:y+zoomed_height, x:x+zoomed_width]

            # Resize the cropped region to the original size with cubic interpolation
            zoomed_frame = cv2.resize(
                zoomed_region, (width, height), interpolation=cv2.INTER_CUBIC)

        else:
            zoomed_frame = frame

        return zoomed_frame


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
    pad: int = 100
    frame_height: int = 0
    frame_width: int = 0


class PaddingProcessor(Processor):
    def __init__(self, data: PaddingData = PaddingData()) -> None:
        super().__init__()
        self.data = data
        frame_width = data.frame_width
        frame_height = data.frame_height
        radius = 10

        background = cv2.imread(ImageUtils.asset(
            'background/background-2.jpg'))

        bh, bw = background.shape[:2]
        # center crop background to fit frame size
        frame_half_w, frame_half_h = frame_width // 2, frame_height // 2
        x1, y1 = bw // 2 - frame_half_w, bh // 2 - frame_half_h
        x2, y2 = x1 + frame_width, y1 + frame_height
        self.cover = background[y1:y2, x1:x2, :].copy()

        ratio = frame_width / frame_height

        pad_y = self.data.pad
        pad_x = int(pad_y * ratio)
        new_height = max(0, frame_height - 2 * pad_y)
        new_width = max(0, frame_width - 2 * pad_x)

        self.pad_x = pad_x
        self.pad_y = pad_y
        self.new_height = new_height
        self.new_width = new_width

        # Draw the rounded rectangle on the mask
        mask = np.zeros((new_height, new_width), dtype=np.uint8)
        cv2.rectangle(mask, (0, radius), (new_width - 1,
                      new_height - radius - 1), 255, -1)
        cv2.rectangle(mask, (radius, 0), (new_width - 1 -
                      radius, new_height - 1), 255, -1)
        cv2.circle(mask, (radius, radius), radius, 255, -1)
        cv2.circle(mask, (radius, new_height - 1 - radius), radius, 255, -1)
        cv2.circle(mask, (new_width - 1 - radius,
                   new_height - 1 - radius), radius, 255, -1)
        cv2.circle(mask, (new_width - 1 - radius, radius), radius, 255, -1)
        self.mask = mask

    def apply(self, frame, frame_index: int):
        resized_frame = cv2.resize(frame, (self.new_width, self.new_height))

        # Apply the mask to the resized frame
        masked_frame = cv2.bitwise_and(
            resized_frame, resized_frame, mask=self.mask)

        # Apply the inverted mask to the cropped background
        cropped_background = self.cover[self.pad_y:self.pad_y +
                                        self.new_height, self.pad_x:self.pad_x+self.new_width, :]
        inv_mask = cv2.bitwise_not(self.mask)
        cropped_background = cv2.bitwise_and(
            cropped_background, cropped_background, mask=inv_mask)

        # Combine the masked frame and the cropped background
        result = cv2.add(masked_frame, cropped_background)
        self.cover[self.pad_y:self.pad_y+self.new_height,
                   self.pad_x:self.pad_x+self.new_width, :] = result
        return self.cover


@dataclass
class VideoProcessorData:
    pass


class VideoProcessor(Processor):
    def __init__(self, video_path: str, mouse_history: Dict[str, List[int]] = None):
        super().__init__()
        self.video_path = video_path
        self.mouse_history = mouse_history

        self.video_capture = cv2.VideoCapture(self.video_path)
        self.frame_rate = int(self.video_capture.get(cv2.CAP_PROP_FPS))
        self.total_frames = int(
            self.video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
        self.frame_height = int(
            self.video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.frame_width = int(
            self.video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))

        zoom_data = []
        print(mouse_history)
        for x, y, frame_index in mouse_history['clicks']:
            interval = frame_index, frame_index + int(1.8 * self.frame_rate)
            zoom_data.append(ZoomData(interval=interval,
                             zoom_factor=2, zoom_center=(x, y)))

        self.processors = [
            ZoomProcessor(data=zoom_data, frame_rate=self.frame_rate),
            PaddingProcessor(
                data=PaddingData(
                    pad=100,
                    frame_height=self.frame_height,
                    frame_width=self.frame_width
                )
            ),
        ]
        self.frame_index = 0

    def get(self, frame_index: int = None):
        if isinstance(frame_index, int):
            self.video_capture.set(cv2.CAP_PROP_POS_FRAMES, frame_index)

        ret, frame = self.video_capture.read()
        if ret:
            t0 = time.time()
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_height, frame_width = frame.shape[:2]
            processed_frame = self.apply(frame, self.frame_index)

            image = QImage(processed_frame, frame_width,
                           frame_height, QImage.Format.Format_RGB888)
            logger.info(f'frame processing time: {time.time() - t0}')
            return image

    def next_frame(self):
        self.frame_index = min(self.frame_index + 1, self.total_frames)
        return self.get(self.frame_index)

    def previous_frame(self):
        self.frame_index = max(self.frame_index - 1, 0)
        self.frame_index = 1
        return self.get(self.frame_index)

    def _build_processors(self) -> List[Processor]:
        pass

    def apply(self, frame, frame_index: int):
        for processor in self.processors:
            frame = processor.apply(frame, frame_index)
        return frame

    def save(self):
        pass

    def export(self):
        pass

# This Python file uses the following encoding: utf-8
import threading, time
from Libs.Common import Common
from abc import ABC, abstractmethod
import numpy as np
import cv2

# Custom decorator to mark a method as final
def final(method):
    method.__is_final__ = True
    return method

class AbstractStreamer(threading.Thread):
    def __init__(self):
        print(f"{Common.func_info()} -----> (AbstractStreamer)")

        self._streamerPath = None
        self._cap = None
        self._fps = -1
        self._framesCount = -1
        self._isInited = False
        self._playbackStatus = False
        self._frameFounded = False
        self._lastFrame = np.zeros((10,10,3), dtype=np.uint8)
        self._frameNumber = -1
    @final
    def exit(self):
        print(f"{Common.func_info()} -----> (AbstractStreamer)")
        self._isInited = False
        self._playbackStatus = False
        self._cap.release()

    @final
    def setStreamerPath(self, newPath):
        print(f"{Common.func_info()} -----> (AbstractStreamer): {newPath}")

        self._streamerPath = newPath
    @final
    def streamerPath(self):
        return self._streamerPath
    
    @abstractmethod
    def init(self):
        print(f"{Common.func_info()} -----> (AbstractStreamer)")
        pass

    @final
    def fps(self):
        return self._fps
    
    @final
    def framesCount(self):
        return self._framesCount

    @final
    def setIsInited(self, status):
        print(f"{Common.func_info()} -----> (AbstractStreamer): {status}")

        self._isInited = status
        if not status:
            self._cap.release()
    @final
    def isInited(self):
        return self._isInited
    
    @final
    def start_thread(self):
        print(f"{Common.func_info()} -----> (AbstractStreamer)")

        self._playbackStatus = True
        super().__init__()
        self.start()
    @final
    def stop_thread(self):
        print(f"{Common.func_info()} -----> (AbstractStreamer)")

        self._playbackStatus = False

    @final
    def run(self):
        if not self._isInited:
            print(f"{Common.func_info()} -----> (AbstractStreamer): Streamer is not inited.")
            return
        print(f"{Common.func_info()} -----> (AbstractStreamer): Streamer thread is started.")

        while self._playbackStatus:
            self.grabFrame()
            time.sleep(0.001) # Sleep for 1 ms

        print(f"{Common.func_info()} -----> (AbstractStreamer): Streamer thread is finished.")

    @abstractmethod
    def grabFrame(self):
        pass
    @abstractmethod
    def retrieveFrame(self):
        pass

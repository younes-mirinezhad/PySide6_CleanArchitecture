import logging
import threading, time
from abc import ABC, abstractmethod
import numpy as np

# Get logger instance
logger = logging.getLogger(__name__)

# Custom decorator to mark a method as final
def final(method):
    method.__is_final__ = True
    return method

class AbstractStreamer(threading.Thread):
    def __init__(self):
        logger.debug("")

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
        logger.debug("")

        self._isInited = False
        self._playbackStatus = False
        self._cap.release()

    @final
    def setStreamerPath(self, newPath):
        logger.info(f"Streamer path: {newPath}")

        self._streamerPath = newPath
    @final
    def streamerPath(self):
        return self._streamerPath
    
    @abstractmethod
    def init(self):
        pass

    @final
    def fps(self):
        return self._fps
    
    @final
    def framesCount(self):
        return self._framesCount

    @final
    def setIsInited(self, status):
        logger.debug(f"Status: {status}")

        self._isInited = status
        if not status:
            self._cap.release()
    @final
    def isInited(self):
        return self._isInited
    
    @final
    def start_thread(self):
        logger.info("")

        self._playbackStatus = True
        super().__init__()
        self.start()
    @final
    def stop_thread(self):
        logger.info("")

        self._playbackStatus = False

    @final
    def run(self):
        if not self._isInited:
            return

        logger.info("Streaming started")

        while self._playbackStatus:
            self.grabFrame()
            time.sleep(0.001) # Sleep for 1 ms

        logger.info("Streaming stopped")

    @abstractmethod
    def grabFrame(self):
        pass
    @abstractmethod
    def retrieveFrame(self):
        pass

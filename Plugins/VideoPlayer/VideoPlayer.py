import logging
from PySide6.QtCore import QObject, Signal, Slot, Property
from Libs.Streamer.VideoFileReader import VideoFileReader
import threading

# Get logger instance
logger = logging.getLogger(__name__)

class VideoPlayer(QObject):
    framesCount_changed = Signal()
    playbackStatus_changed = Signal()
    frameNumber_changed = Signal()

    def __init__(self) -> None:
        super().__init__()
        logger.debug("")
        self.name = "VideoPlayer"
        self.uiUrl = "VideoPlayer.qml"
        self.iconUrl = "VideoPlayer.png"
        self.order = 2

        self.viewPort = None
        self._streamerPath = None
        self.streamer = None
        self._framesCount = 0
        self._playbackStatus = False
        self._timeInterval = 0
        self._frameNumber = 0

    @Slot()
    def exit(self):
        logger.debug("")

        self._timeInterval = 0
        if self.streamer:
            self.streamer.exit()

    @Slot(QObject)
    def setViewPort(self, viewPortObj):
        logger.debug("")

        self.viewPort = viewPortObj

    @Slot(str)
    def setStreamerPath(self, newPath):
        logger.info(f"StreamerPath: {newPath}")

        self._streamerPath = newPath

    @Slot()
    def init(self):
        logger.info("")

        vfr = VideoFileReader()
        vfr.setStreamerPath(self._streamerPath)
        vfr.init()
        self.framesCount = vfr.framesCount()

        self.streamer = vfr

    def set_framesCount(self, fCount):
        logger.info(f"framesCount: {fCount}")

        self._framesCount = fCount
        self.framesCount_changed.emit()
    def get_framesCount(self):
        return self._framesCount
    framesCount = Property(int, get_framesCount, set_framesCount, notify=framesCount_changed)

    @Slot()
    def changeStreamerStatus(self):
        logger.debug("")

        if not self.streamer:
            return
        if not self.streamer.isInited():
            return

        self.playbackStatus = not self._playbackStatus

        if self._playbackStatus:
            self.streamer.start_thread()
            self._timeInterval = 1 / self.streamer.fps()
            threading.Timer(self._timeInterval, self.readFrames).start()
        else:
            self.streamer.stop_thread()
            self._timeInterval = 0
    
    def set_playbackStatus(self, status):
        logger.debug("")

        self._playbackStatus = status
        self.playbackStatus_changed.emit()
    def get_playbackStatus(self):
        return self._playbackStatus
    playbackStatus = Property(bool, get_playbackStatus, set_playbackStatus, notify=playbackStatus_changed)

    def readFrames(self):
        if self._timeInterval > 0:
            fNum, f = self.streamer.retrieveFrame()
            self.viewPort.setNewFrame(f)
            self.frameNumber = fNum
            threading.Timer(self._timeInterval, self.readFrames).start()
    
    def set_frameNumber(self, fNum):
        logger.debug(f"frameNumber: {fNum}")

        self._frameNumber = fNum
        self.frameNumber_changed.emit()
    def get_frameNumber(self):
        return self._frameNumber
    frameNumber = Property(int, get_frameNumber, set_frameNumber, notify=frameNumber_changed)

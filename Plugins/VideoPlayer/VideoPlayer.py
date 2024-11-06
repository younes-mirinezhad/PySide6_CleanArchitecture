from PySide6.QtCore import QObject, Signal, Slot, Property
from Libs.Common import Common
from Libs.Streamer.VideoFileReader import VideoFileReader
import threading

class VideoPlayer(QObject):
    framesCount_changed = Signal()
    playbackStatus_changed = Signal()
    frameNumber_changed = Signal()

    def __init__(self) -> None:
        print(Common.func_info())
        super().__init__()
        self.name = "VideoPlayer"
        self.uiUrl = "VideoPlayer.qml"
        self.iconUrl = "VideoPlayer.png"
        self.order = 2

        self._viewPort = None
        self._streamerPath = None
        self._streamer = None
        self._framesCount = 0
        self._playbackStatus = False
        self._timeInterval = 0
        self._frameNumber = 0

    @Slot()
    def exit(self):
        print(Common.func_info())
        self._timeInterval = 0
        if self._streamer:
            self._streamer.exit()

    @Slot(QObject)
    def setViewPort(self, viewPortObj):
        print(Common.func_info())

        self._viewPort = viewPortObj

    @Slot(str)
    def setStreamerPath(self, newPath):
        print(f"{Common.func_info()} -----> Path: {newPath}")

        self._streamerPath = newPath

    @Slot()
    def init(self):
        print(Common.func_info())

        vfr = VideoFileReader()
        vfr.setStreamerPath(self._streamerPath)
        vfr.init()
        self.set_framesCount(vfr.framesCount())

        self._streamer = vfr

    def set_framesCount(self, fCount):
        self._framesCount = fCount
        self.framesCount_changed.emit()
    def get_framesCount(self):
        return self._framesCount
    framesCount = Property(int, get_framesCount, set_framesCount, notify=framesCount_changed)

    @Slot()
    def changeStreamerStatus(self):
        if not self._streamer:
            print(f"{Common.func_info()} -----> Streamer is not inited.")
            return
        if not self._streamer.isInited():
            print(f"{Common.func_info()} -----> Streamer is not inited.")
            return
        print(Common.func_info())

        self.playbackStatus = not self._playbackStatus

        if self._playbackStatus:
            self._streamer.start_thread()
            self._timeInterval = 1 / self._streamer.fps()
            threading.Timer(self._timeInterval, self.readFrames).start()
        else:
            self._streamer.stop_thread()
            self._timeInterval = 0
    
    def set_playbackStatus(self, status):
        print(f"{Common.func_info()} -----> status: {status}")

        self._playbackStatus = status
        self.playbackStatus_changed.emit()
    def get_playbackStatus(self):
        return self._playbackStatus
    playbackStatus = Property(bool, get_playbackStatus, set_playbackStatus, notify=playbackStatus_changed)

    def readFrames(self):
        if self._timeInterval > 0:
            fNum, f = self._streamer.retrieveFrame()
            self._viewPort.setNewFrame(f)
            self.frameNumber = fNum
            threading.Timer(self._timeInterval, self.readFrames).start()
    
    def set_frameNumber(self, fNum):
        self._frameNumber = fNum
        self.frameNumber_changed.emit()
    def get_frameNumber(self):
        return self._frameNumber
    frameNumber = Property(int, get_frameNumber, set_frameNumber, notify=frameNumber_changed)

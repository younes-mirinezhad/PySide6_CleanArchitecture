import logging
from Libs.Streamer.AbstractStreamer import AbstractStreamer
import cv2

# Get logger instance
logger = logging.getLogger(__name__)

class VideoFileReader(AbstractStreamer):
    def __init__(self) -> None:
        super().__init__()
        logger.debug("")

    def init(self):
        logger.info("")

        self._cap = cv2.VideoCapture(self._streamerPath)

        if not self._cap.isOpened():
            return
        
        self._fps = round(self._cap.get(cv2.CAP_PROP_FPS))
        self._framesCount = round(self._cap.get(cv2.CAP_PROP_FRAME_COUNT))

        self.setIsInited(True)

    def grabFrame(self):
        if self._frameFounded:
            return
        
        ret, frame = self._cap.read()
        if ret and min(frame.shape[0], frame.shape[1]) > 0:
            self._frameFounded = True
            self._lastFrame = frame
            self._frameNumber = round(self._cap.get(cv2.CAP_PROP_POS_FRAMES))
    
    def retrieveFrame(self):
        f = self._lastFrame
        fNum = self._frameNumber
        self._frameFounded = False

        return fNum, f
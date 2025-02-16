import os


class Config:
    def __init__(self):
        self.root_dir = os.getenv("MEDIA_ROOT", r"/mnt/c/temp/subtitles").rstrip("/")
        self.scan_interval = os.getenv("SCAN_INTERVAL", 60)
        self.file_infix = os.getenv("FILE_INFIX", "ffsubsync")

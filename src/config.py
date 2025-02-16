import os


class Config:
    def __init__(self):
        self.root_dir = os.getenv("MEDIA_ROOT").rstrip("/")
        self.scan_interval = int(os.getenv("SCAN_INTERVAL", 60))
        self.file_infix = os.getenv("FILE_INFIX", "ffsubsync")

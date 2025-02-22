import os


class Config:
    def __init__(self):
        try:
            self.video_directory = os.environ["VIDEO_DIRECTORY"].rstrip("/")
            self.scan_interval = int(os.getenv("SCAN_INTERVAL", 60))
            self.sync_marker = os.getenv("SYNC_MARKER", "ffsubsync")
            self.delete_source_sub = self._parse_bool(os.getenv("DELETE_SOURCE_SUB", "False"))
        except KeyError as e:
            raise RuntimeError(f"Missing required environment variable: {e}") from e
        except ValueError as e:
            raise RuntimeError(f"Invalid value for SCAN_INTERVAL, must be an integer.") from e
        except Exception as e:
            raise RuntimeError(f"Unexpected error loading configuration: {e}") from e

    @staticmethod
    def _parse_bool(value: str) -> bool:
        """Convert an environment variable string to a boolean."""
        return value.lower() in {"1", "true", "yes", "on"}

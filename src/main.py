import time
import subprocess
from pathlib import Path

from custom_logger import get_logger
from config import Config

logger = get_logger(__name__)

VIDEO_FORMATS = (".mkv", ".mp4")


def get_video_files(root_dir: Path) -> list[Path]:
    """Get all video files recursively from the given directory."""
    return [file for ext in VIDEO_FORMATS for file in root_dir.rglob(f"*{ext}")]


def get_matching_subtitles(video_path: Path) -> list[Path]:
    """Find subtitle files matching a video, allowing multiple extensions before .srt."""
    base_name = video_path.with_suffix('')  # Remove only the last extension
    subtitle_files = []

    for sub_file in video_path.parent.glob("*.srt"):
        if sub_file.stem.startswith(base_name.stem):  # Match base name (ignoring extensions)
            subtitle_files.append(sub_file)

    return subtitle_files


def is_synced_subtitles(filename: Path, file_infix: str) -> bool:
    """Check if a subtitle file is already synced."""
    return file_infix in filename.stem


def rename_subtitles(filename: Path, file_infix: str) -> Path:
    """Generate a new subtitle filename with the sync infix."""
    return filename.with_stem(f"{filename.stem}.{file_infix}")


def sync_subtitles(in_video: Path, in_sub: Path, out_sub: Path) -> bytes:
    """Synchronize subtitles using ffsubsync."""
    logger.debug(
        f"\nVideo: {in_video.name}\nSubtitle: {in_sub.name}\nOutput: {out_sub.name}"
    )
    try:
        result = subprocess.run(
            ["ffsubsync", str(in_video), "-i", str(in_sub), "-o", str(out_sub)],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.encode()
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to sync subtitles: {e}")
        return b""


def main(config: Config):
    """Main processing loop for finding and syncing subtitles."""
    root_dir = Path(config.root_dir)

    videos = get_video_files(root_dir)
    for video in videos:
        for sub in get_matching_subtitles(video):
            if is_synced_subtitles(sub, config.file_infix):
                continue

            new_sub = rename_subtitles(sub, config.file_infix)
            if new_sub.exists():
                continue

            sync_subtitles(video, sub, new_sub)


if __name__ == "__main__":
    config = Config()
    while True:
        logger.debug("Scanning files.")
        main(config)
        logger.debug("Sleeping.")
        time.sleep(config.scan_interval)

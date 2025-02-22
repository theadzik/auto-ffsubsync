import time
import subprocess
from pathlib import Path

from custom_logger import get_logger
from config import Config

logger = get_logger(__name__)

VIDEO_FORMATS = (".mkv", ".mp4")


def find_video_files(video_directory: Path) -> list[Path]:
    """Recursively find all video files in the given directory."""
    return [file for ext in VIDEO_FORMATS for file in video_directory.rglob(f"*{ext}")]


def find_subtitle_files(video_file: Path) -> list[Path]:
    """Find subtitle files matching a video, allowing multiple extensions before .srt."""
    base_name = video_file.with_suffix('')  # Remove only the last extension
    subtitle_files = []

    for subtitle_file in video_file.parent.glob("*.srt"):
        if subtitle_file.stem.startswith(base_name.stem):  # Match base name (ignoring extensions)
            subtitle_files.append(subtitle_file)

    return subtitle_files


def is_subtitle_synced(subtitle_file: Path, sync_marker: str) -> bool:
    """Check if a subtitle file is already synced."""
    return sync_marker in subtitle_file.stem


def generate_synced_subtitle_path(subtitle_file: Path, sync_marker: str) -> Path:
    """Generate a new subtitle filename with the sync marker."""
    return subtitle_file.with_stem(f"{subtitle_file.stem}.{sync_marker}")


def synchronize_subtitles(video_file: Path, subtitle_file: Path, output_subtitle: Path) -> bytes:
    """Synchronize subtitles using ffsubsync."""
    logger.debug(
        f"\nVideo: {video_file.name}\nSubtitle: {subtitle_file.name}\nOutput: {output_subtitle.name}"
    )
    try:
        result = subprocess.run(
            ["ffsubsync", str(video_file), "-i", str(subtitle_file), "-o", str(output_subtitle)],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.encode()
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to sync subtitles: {e}")
        return b""


def main(config: Config):
    """Main processing loop for finding and synchronizing subtitles."""
    video_directory = Path(config.video_directory)

    video_files = find_video_files(video_directory)
    for video_file in video_files:
        for subtitle in find_subtitle_files(video_file):
            if is_subtitle_synced(subtitle, config.sync_marker):
                logger.debug(f"Already synced: {subtitle}")
                continue

            synced_subtitle = generate_synced_subtitle_path(subtitle, config.sync_marker)
            if synced_subtitle.exists():
                logger.debug(f"Already synced in another file: {subtitle}")
                continue

            synchronize_subtitles(video_file, subtitle, synced_subtitle)
            if config.delete_source_sub:
                try:
                    subtitle.unlink()
                    logger.info(f"Deleted original subtitle: {subtitle}")
                except Exception as e:
                    logger.error(f"Failed to delete subtitle {subtitle}: {e}")


if __name__ == "__main__":
    config = Config()
    while True:
        logger.debug("Scanning for files.")
        main(config)
        logger.debug("Sleeping.")
        time.sleep(config.scan_interval)

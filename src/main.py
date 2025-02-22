import glob
import os
import time
import subprocess

from custom_logger import get_logger
from config import Config

logger = get_logger(__name__)

configuration = Config()

VIDEO_FORMATS = ("*.mkv", "*.mp4",)


def get_video_files() -> list:
    video_files = []
    for video_format in VIDEO_FORMATS:
        video_files.extend(glob.glob(configuration.root_dir + "/**/" + video_format, recursive=True))
    return video_files


def get_matching_subtitles(video_path) -> list:
    matching_subtitles = []
    base_name = get_base_file_name(video_path)
    matching_subtitles.extend(glob.glob(glob.escape(base_name) + "*.srt"))
    return matching_subtitles


def get_base_file_name(file_name: str) -> str:
    return ".".join(file_name.split(".")[0:-1])


def is_synced_subtitles(filename: str) -> bool:
    return configuration.file_infix in filename


def rename_subtitles(filename: str):
    split_name = filename.split(".")
    split_name.insert(-1, configuration.file_infix)
    new_name = ".".join(split_name)
    return new_name


def sync_subtitles(in_video: str, in_sub: str, out_sub: str) -> bytes:
    logger.debug(
        f"\nin_video: {os.path.basename(in_video)}"
        f"\nin_sub: {os.path.basename(in_sub)}"
        f"\nout_sub: {os.path.basename(out_sub)}"
    )
    args = ("ffsubsync", in_video, "-i", in_sub, "-o", out_sub)
    popen = subprocess.Popen(args, stdout=subprocess.PIPE)
    popen.wait()
    output = popen.stdout.read()
    return output


def main():
    videos = get_video_files()
    for v in videos:
        subtitle_files = get_matching_subtitles(v)
        for subs in subtitle_files:
            if is_synced_subtitles(subs):
                continue
            new_subs = rename_subtitles(subs)
            if os.path.isfile(new_subs):
                continue
            sync_subtitles(v, subs, new_subs)


while True:
    logger.debug("Scanning files.")
    main()
    logger.debug("Sleeping.")
    time.sleep(configuration.scan_interval)

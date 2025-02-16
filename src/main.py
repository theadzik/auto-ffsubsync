import glob
import os
import time
import subprocess

from custom_logger import get_logger
from config import Config

logger = get_logger(__name__)

configuration = Config()

VIDEO_FORMATS = ["mkv", "mp4", ]


def get_file_pairs():
    for sub_file in glob.iglob(configuration.root_dir + '/**/*.pol.srt', recursive=True):
        logger.debug(f"Found sub file: {os.path.basename(sub_file)}")
        if os.path.isfile(rename_subtitles(sub_file)):
            logger.debug(f"Already synced!")
            continue
        base_glob = glob.escape(".".join(sub_file.split(".")[0:-2])) + "*" # Glob excluding .pol.srt part of the filename
        for video_file in glob.iglob(base_glob):
            for video_format in VIDEO_FORMATS:
                if video_file.endswith(video_format):
                    logger.info(f"Found video: {os.path.basename(video_file)}")
                    yield video_file, sub_file


def rename_subtitles(filename: str):
    split_name = filename.split(".")
    split_name.insert(-1, configuration.file_infix)
    new_name = ".".join(split_name)
    return new_name


def sync_subtitles(in_video: str, in_sub: str, out_sub: str):
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


while True:
    logger.debug("Scanning files.")
    for video, subs in get_file_pairs():
        new_subs = rename_subtitles(subs)
        out = sync_subtitles(video, subs, new_subs)
    logger.debug("Sleeping.")
    time.sleep(configuration.scan_interval)

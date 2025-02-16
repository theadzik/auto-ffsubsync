import glob
from custom_logger import get_logger

from config import Config
import subprocess

logger = get_logger(__name__)

configuration = Config()

VIDEO_FORMATS = ["mkv", "mp4", ]

def get_file_pairs():
    for filename in glob.iglob(configuration.root_dir + '/**/*.pol.srt', recursive=True):
        logger.debug(f"Found sub file: {filename}")
        base_name = ".".join(filename.split(".")[0:-2])
        for glob_file in glob.iglob(base_name + "*"):
            logger.debug(f"Checking if {glob_file} is a video")
            for video_format in VIDEO_FORMATS:
                if glob_file.endswith(video_format):
                    logger.debug("It is!")
                    yield glob_file, filename

def rename_subtitles(filename: str):
    split_name = filename.split(".")
    split_name.insert(-1, configuration.file_infix)
    new_name = ".".join(split_name)
    return new_name

def sync_subtitles(in_video: str, in_sub: str, out_sub: str):
    logger.debug(f"in_video: {in_video}\nin_sub: {in_sub}\n out_sub: {out_sub}")
    args = ("ffsubsync", in_video, "-i", in_sub, "-o", out_sub)
    popen = subprocess.Popen(args, stdout=subprocess.PIPE)
    popen.wait()
    output = popen.stdout.read()
    return output

for video, subs in get_file_pairs():
    new_subs = rename_subtitles(subs)

    out = sync_subtitles(video, subs, new_subs)
    logger.info(f"ffsubsync output:\n{out}")

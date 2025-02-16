import glob
import time
import logging

from config import Config
import subprocess

configuration = Config()

VIDEO_FORMATS = ["mkv", "mp4", ]

def get_file_pairs():
    for filename in glob.iglob(configuration.root_dir + '/**/*.pol.srt', recursive=True):
        base_name = ".".join(filename.split(".")[0:-2])
        for glob_file in glob.iglob(base_name + "*"):
            for video_format in VIDEO_FORMATS:
                if glob_file.endswith(video_format):
                    yield glob_file, filename

def rename_subtitles(filename: str):
    split_name = filename.split(".")
    split_name.insert(-1, configuration.file_infix)
    new_name = ".".join(split_name)
    return new_name

def sync_subtitles(in_video: str, in_sub: str, out_sub: str):
    args = ("ffsubsync", in_video, "-i", in_sub, "-o", out_sub)
    popen = subprocess.Popen(args, stdout=subprocess.PIPE)
    popen.wait()
    output = popen.stdout.read()
    return output

for video, subs in get_file_pairs():
    new_subs = rename_subtitles(subs)

    out = sync_subtitles(video, subs, new_subs)
    print(out)

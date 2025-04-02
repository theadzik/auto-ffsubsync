# auto-ffsubsync

**This little experiment is no longer maintained. I switched to bazarr**

A service that syncs subtitles with movies using [ffsubsync](https://github.com/smacke/ffsubsync)

It works with automatically downloaded subtitles in Jellyfin by OpenSubtitles plugin.
It's super-early version, so it only works if the `.srt` file name matches the video name.
It also only works with subtitle files ending with `.pol.srt` because I hardcoded it that way for simplicity.

----

Configuration:

| Env var           | Required | Default   | Description                                |
|-------------------|----------|-----------|--------------------------------------------|
| VIDEO_DIRECTORY   | Yes      | -         | Path to directory with videos to scan      |
| LOG_LEVEL         | No       | INFO      | Level of logging \( DEBUG \| INFO \)       |
| SCAN_INTERVAL     | No       | 60        | Number of seconds between scans            |
| SYNC_MARKER       | No       | ffsubsync | String added to synced subtitles filenames |
| DELETE_SOURCE_SUB | No       | False     | Remove original subtitles file             |

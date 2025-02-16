# auto-ffsubsync

A service that syncs subtitles with movies using [ffsubsync](https://github.com/smacke/ffsubsync)

It works with automatically downloaded subtitles in Jellyfin by OpenSubtitles plugin.
It's super-early version, so it only works if the `.srt` file name matches the video name.
It also only works with subtitle files ending with `.pol.srt` because I hardcoded it that way for simplicity.

----

Configuration:

| Env var       | Required | Default   | Description                               |
|---------------|----------|-----------|-------------------------------------------|
| MEDIA_ROOT    | Yes      | -         | Path to directory with videos to scan     |
| LOG_LEVEL     | No       | DEBUG     | Level of logging \( DEBUG \| INFO \)      |
| SCAN_INTERVAL | No       | 60        | Number of seconds between scans           |
| FILE_INFIX    | No       | ffsubsync | String added to synced subtitle filenames |

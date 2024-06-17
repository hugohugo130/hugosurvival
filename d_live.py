import subprocess
from module.getxiaozilivelink import getlink
from os import remove
from os.path import exists
if exists("video.mp4"):
    print("影片存在,正在刪除...")
    remove("video.mp4")
livelink = getlink()
subprocess.run(
    [
        "streamlink",
        "--hls-live-edge",
        "99999",
        "--hls-segment-threads",
        "5",
        "-o",
        "video.mp4",
        livelink,
        "best",
    ]
)
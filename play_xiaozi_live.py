import vlc
import time
from os.path import exists

# creating vlc media player object
media_player = vlc.MediaPlayer()

# media object
media = vlc.Media("video.mp4")

# setting media to the media player
media_player.set_media(media)


# start playing video
media_player.play()

while True:
    if not exists("stopplay.txt"):
        time.sleep(1)

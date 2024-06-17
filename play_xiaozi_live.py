# importing vlc module
import vlc

# importing time module
import time


# creating vlc media player object
media_player = vlc.MediaPlayer()

# media object
media = vlc.Media("video.mp4")

# setting media to the media player
media_player.set_media(media)


# start playing video
media_player.play()

while True:
    time.sleep(1)
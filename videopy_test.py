from moviepy.editor import VideoClip
from moviepy.editor import VideoFileClip
from moviepy.editor import ImageClip
# https://zulko.github.io/moviepy/getting_started/compositing.html#stacking-and-concatenating-clips
from moviepy.editor import concatenate_videoclips, clips_array

def video():
    clip1 = ImageClip("./simplesignage/manager/static/content/c1/Lake-Chelan.jpeg")
    clip1.set_fps(15) # framerate
    clip1 = clip1.set_end(15) # duration: 0 to n=15 seconds
    #clip1.resize(height=1080) # height of the clip
    clip2 = ImageClip("./simplesignage/manager/static/content/c2/Mount-Rainier.jpg")
    clip2 = clip2.set_end(10)
    #clip2.resize(height=1080)
    clip2.set_fps(15)
    clip3 = ImageClip("./simplesignage/manager/static/content/c3/mt-stuart.jpg")
    clip3 = clip3.set_end(10)
    #clip3.resize(height=1080)
    clip3.set_fps(15)
    clip4 = VideoFileClip("./simplesignage/manager/static/content/c9/ENBjQKJ_-_Imgur.mp4")

    final = concatenate_videoclips(clips=[clip1, clip4, clip2, clip3], method="compose")
    final.resize(height=1080)
    final.write_videofile(filename="./video.mp4", fps=15, audio=False)#, progress_bar=True)

if __name__ == "__main__":
    video()

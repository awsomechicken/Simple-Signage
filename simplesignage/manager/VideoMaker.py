# !/usr/bin/python3
# python lib for video creation from videos and pictures
# Author: R. Sanford
# Date: 23 July 2019

import os, time

# import moviepy:
try:
    from moviepy.editor import VideoClip
    from moviepy.editor import VideoFileClip

except:
    print("Error loading MoviePy, please install:\n\t~$ pip install moviepy")


# get first frame for a thumbnail
def get_thumbnail(abs_path="./static/content", file_name="animals-Imgur.mp4"):
    print("thumbnail generating...")
    img_name = file_name[0:file_name.rindex('.')]+".jpg" # make-up the new image file
    print(img_name)
    if abs_path[len(abs_path)-1] == '/':
        video_path = "%s%s"%(abs_path, file_name)
        thumbnail_path = ".%s%s"%(abs_path, img_name)
    else:
        video_path = ".%s/%s"%(abs_path, file_name)
        thumbnail_path = ".%s/%s"%(abs_path, img_name)

    video = VideoFileClip(video_path) # get the file from the absolute path
    video.save_frame(thumbnail_path, t=0)
    print("Thumbnail complete.")

    return img_name # return the name of the file.

def compile_video(show_items={}, output_path='./static/shows/', frame_rate=30):
    # items: {{path, time}, ...}
    print("Compiling Video...")

    name = "Show_%d"%(int(time.time()))
    print(name)
    if path.rindex('/') == len(output_path)-1:
        showPath = "%s%s.mp4"%(output_path, name)
    else:
        showPath = "%s/%s.mp4"%(output_path, name)
    video = VideoClip()
    video.fps=frame_rate

    for item in items:
        if ".mp4" in  item.file.lower():
            print("Video: ", item.file)

        elif ".pdf" in item.file.lower():
            print("PDF: ", item.file)

        elif ".png" or ".jpg" in item.file.lower():
            print("Image: ", item.file)

        else:
            print("unsupported file type: ", item.file.lower()[item.file.rindex('.'):len(item.file)])

    return showPath


if __name__ == "__main__":
    print("Processing...")
    #get_mp4_thumbnail();
    compile_video()

# !/usr/bin/python3
# python lib for video creation from videos and pictures
# Author: R. Sanford
# Date: 23 July 2019

import os, time

# import moviepy:
try:
    from moviepy.editor import VideoClip
    from moviepy.editor import VideoFileClip
    from moviepy.editor import ImageClip
    # https://zulko.github.io/moviepy/getting_started/compositing.html#stacking-and-concatenating-clips
    from moviepy.editor import concatenate_videoclips

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

def compile_video(show_items, output_path='./manager/static/shows/', frame_rate=30):
    # items: {item 1, item 2, ...}
    print("Compiling Video...")

    name = "Show_%d.mp4"%(int(time.time()))
    print(name)

    if output_path.rindex('/') == len(output_path)-1:
        showPath = "%s%s"%(output_path, name)
    else:
        showPath = "%s/%s"%(output_path, name)

    video_clips = [] # clip array, will use a SHIT LOAD of memory, you're editing a video...

    for item in show_items:
        if os.path.isfile(item.file):
            # debug params
            #print("file: ", item.file, "Exists")
            #print(os.listdir(item.file[0:item.file.rindex('/')+1]))

            if ".mp4" in item.file.lower():
                # Use VideoFileClip class
                vclip = VideoFileClip(item.file)
                # resize the height to 1080p
                vclip = vclip.resize(height=1080)
                # then see if it is too wide
                (w, h) = vclip.size
                if w > 1920:
                    vclip = vclip.resize(width=1920)
                    print("resize width")
                video_clips.append(vclip)

            elif ".gif" in item.file.lower():
                # Use VideoFileClip class
                vclip = VideoFileClip(item.file)
                # resize the height to 1080p
                vclip = vclip.resize(height=1080)
                # then see if it is too wide
                (w, h) = vclip.size
                if w > 1920:
                    vclip = vclip.resize(width=1920)
                    print("resize width")
                #vclip.set_fps(frame_rate)
                for gi in range(0, item.gifIteration):
                    video_clips.append(vclip)

            elif ".png" or ".jpg" in item.file.lower():
                # Use ImageClip class
                img = ImageClip(item.file)
                # resize the height to 1080p
                img = img.resize(height=1080)
                # then if it is too wide, resize to 1920 wide
                (w, h) = img.size
                if w > 1920:
                    img = img.resize(width=1920)
                    print("resize width")
                #img.resize(height=1080)
                img = img.set_end(int(item.displayTime))
                #img.set_fps(frame_rate)
                video_clips.append(img)

            else:
                print("unsupported file type: ", item.file.lower()[item.file.rindex('.'):len(item.file)])
        else:
            print("File: ", item.file, "Does Not Exist")

        #elif ".pdf" in item.file.lower(): # pdf are taken care of at upload
        #    print("PDF: ", item.file)
        # pause last frame and fade out/in?

    final_clip = concatenate_videoclips(video_clips, method="compose")
    final_clip.resize(height=1080)
    final_clip.write_videofile(filename=showPath, fps=frame_rate, audio=False, threads=4)
    return showPath, name


if __name__ == "__main__":
    print("Processing...")
    #get_mp4_thumbnail();
    compile_video()

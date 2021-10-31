import os
from moviepy.editor import *
from pytube import YouTube


def audio_video_file():
    audioclip = AudioFileClip('aud.wav')
    videoclip = VideoFileClip('vid.mp4')
    videoclip2 = videoclip.set_audio(audioclip)
    videoclip2.write_videofile('output.mp4')
    os.remove('aud.wav')
    os.remove('vid.mp4')


video_url = input("Enter YouTube Video URL: ")
youtube_obj = YouTube(video_url)
my_streams = youtube_obj.streams

print("-" * 60)
print("All the available resolutions are ", (list(set([res for res in [
      stream.resolution for stream in my_streams.filter(progressive=False)] if res]))))
print(
    "Choose between the following progressive streams resolution ", [
        stream.resolution for stream in my_streams.filter(
            progressive=True)], "for best results")
print("You can still choose other resolution but muxing is done for non-progressive streams and it takes some time to process the files")
print("-" * 60)

video_res = input(
    f"Enter YouTube Video Resolution for {youtube_obj.title}: ").strip()

if video_res[-1] != "p":
    video_res = video_res + "p"

downloaded = False
# if required stream is progressive
if video_res in [
    stream.resolution for stream in my_streams.filter(
        progressive=True)]:
    if video_res == "144p":
        req_stream = my_streams.get_by_itag(17)
    else:
        req_stream = my_streams.get_by_resolution(video_res)
    req_stream.download(filename='output.mp4')
    downloaded = True

# if not, download video stream and audio seprately and combine
else:
    my_streams.filter(res=video_res).first().download(filename='vid.mp4')
    my_streams.filter(only_audio=True).first().download(filename='aud.wav')

    print("Downloaded the following streams:")
    print(my_streams.filter(res=video_res).first())
    print(my_streams.filter(only_audio=True).first())

    audio_video_file()
    downloaded = True

if downloaded:
    print("Download complete!")
else:
    print("Download Failed")

import pysrt
from moviepy import VideoFileClip, TextClip, CompositeVideoClip
from moviepy.video.tools.subtitles import SubtitlesClip
import os
# 1. Define a function to convert SRT time objects to seconds
def time_to_seconds(time_obj):
    return time_obj.hours * 3600 + time_obj.minutes * 60 + time_obj.seconds + time_obj.milliseconds / 1000.0

# 2. Define a generator function for the subtitle clips
# This function creates a TextClip for each subtitle entry, allowing styling
def subtitles_generator(txt,video_clip):
    text_clip = TextClip(text=txt, font='C:/Windows/Fonts/arial.ttf', font_size=30, color='white', stroke_color='black', stroke_width=1.5, method='caption', text_align='center', size=(video_clip.w - 20, None))
    text_clip = text_clip.with_position(('center', video_clip.h-50))
    return text_clip

# 3. Load the video file
def extract_video_subtitles(video_path,subtitle_path,lang):
    filename,ext=os.path.splitext(os.path.basename(video_path).split('/')[-1])
    video_clip = VideoFileClip(video_path)

    subs = pysrt.open(subtitle_path)
    subtitle_clips = []
    for subtitle in subs:
        start_time = time_to_seconds(subtitle.start)
        end_time = time_to_seconds(subtitle.end)
        duration = end_time - start_time
        # Generate the text clip and set its duration and start time
        text_clip = subtitles_generator(subtitle.text,video_clip)
        text_clip = text_clip.with_start(start_time).with_duration(duration)
        subtitle_clips.append(text_clip)

    # 5. Composite the video and subtitle clips
    # The final video is a composition of the original video and all the subtitle clips
    final_clip = CompositeVideoClip([video_clip] + subtitle_clips)

    # 6. Write the final video file
    final_clip.write_videofile(f"./output/{filename}_{lang}.mp4", codec="libx264", audio_codec="aac")

    # 7. Close the clips
    video_clip.close()
    final_clip.close()
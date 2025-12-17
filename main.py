from utils.extract_audio import convert_video_to_audio_moviepy
from utils.transcribe import transcribe_audio_openai
from utils.translate import translate
from utils.extract_sub_video import extract_video_subtitles
import os
import srt
import argparse
def list_of_strings(arg):
    return arg.split(',')

def get_translated_filename(video_path,lang):
    filename,ext=os.path.splitext(os.path.basename(video_path).split('/')[-1])
    return f"./extracted_subtitles/{filename}_{lang}.srt"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Translate video files")
    parser.add_argument("-v","--video_path", help="Video files",type=str)
    parser.add_argument("-l", "--language", help="Specify the language", default="vietnamese", type=list_of_strings)
    args = parser.parse_args()
    video_path=args.video_path
    languages=args.language
    convert_video_to_audio_moviepy(video_path)
    filename, ext = os.path.splitext(video_path)
    audio_path=f"{filename}.mp3"
    segments = transcribe_audio_openai(audio_path)
    subs = list(srt.parse(segments))
    for lang in languages:
        lang=lang.strip() 
        clone_subs=subs.copy()
        translate(clone_subs,target_language=lang)
        output = srt.compose(clone_subs)
        with open(get_translated_filename(video_path,lang),"w", encoding="utf-8") as handle:
            handle.write(output)
        extract_video_subtitles(video_path,get_translated_filename(video_path,lang),lang)
    
        
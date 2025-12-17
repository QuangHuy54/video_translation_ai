import json
from dotenv import load_dotenv
import srt
from moviepy import VideoFileClip
from openai import OpenAI
from prompt import SYSTEM_PROMPT
import os
import math
import base64
load_dotenv()

MODEL = "gpt-3.5-turbo"
VERBOSE = False
BATCHSIZE = 50

client = OpenAI()

def load_image_base64(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

def makebatch(chunk):
    return [x.content for x in chunk]

def extract_frames_from_batch(chunk, video_path,batch_id):
    #filename, ext = os.path.splitext(video_path)
    clip = VideoFileClip(video_path)
    t_min = min(sub.start for sub in chunk).total_seconds()
    t_max = max(sub.end   for sub in chunk).total_seconds()
    images_path=[]
    for i in range(math.floor(t_min),math.ceil(t_max)):
        out = f"../extracted_frames/frame_{batch_id}_{i}.jpg"
        images_path.append(out)
        clip.save_frame(out, t=i)
    return images_path

def translate_batch(batch, target_language):
    tbatch = []
    blen = len(batch)
    lendiff = 1
    batch=json.dumps(batch, ensure_ascii=False),
    while lendiff != 0: 
        try:
            completion = client.chat.completions.create(model=MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT + f"Translate the text below line by line into {target_language}. "},
                {"role": "user", "content": batch}
            ])
            tbatch = json.loads(completion.choices[0].message.content)
        except Exception as e:
            if VERBOSE:
                print(e)
            lendiff = 1
        else:
            lendiff = len(tbatch) - blen
    return tbatch

def translate(subs,target_language,video_path=None):
    total_batch = (len(subs) + BATCHSIZE - 1) // BATCHSIZE
    for i in range(0, len(subs), BATCHSIZE):
        print(f"batch {i//BATCHSIZE + 1} / {total_batch}")
        chunk = subs[i:i+BATCHSIZE]
        batch = makebatch(chunk)
        # images_paths=extract_frames_from_batch(chunk,video_path,i)
        # content = []
        # for image in images_paths:
        #     content.append({
        #         "type": "input_image",
        #         "image_base64": load_image_base64(image)
        #     })
        # content.append({
        #     "type":"text",
        #     "text": json.dumps(batch, ensure_ascii=False),
        # })
        batch = translate_batch(batch,target_language)
        for j, n in enumerate(batch):
            chunk[j].content = n

if __name__ == "__main__":
    # transcript_srt='''\
    #     1
    #     00:00:00,000 --> 00:00:09,160
    #     It's so cold today. Yes, it's a bit chilly.

    #     2
    #     00:00:09,160 --> 00:00:12,920
    #     It's twenty-five degrees. What would that be in England?

    #     3
    #     00:00:12,920 --> 00:00:17,799
    #     Oh, minus something. But how did you know I was English?

    #     4
    #     00:00:17,799 --> 00:00:21,000
    #     Well, I could tell by your accent. Oh.
    #     '''
    from transcribe import transcribe_audio_openai
    audio_file = "D:\\Project web\\video_translation_ai\\input\\test1.mp3"
    video_file= "D:\\Project web\\video_translation_ai\\input\\test1.mp4"
    segments = transcribe_audio_openai(audio_file)

    subs = list(srt.parse(segments))
    translate(subs,target_language="VN",video_path=video_file)
    output = srt.compose(subs)
    print(output)
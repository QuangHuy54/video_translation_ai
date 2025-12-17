# 🧠 Process Documentation – AI-Powered Video Translation Tool

## 1. Goal

The objective of this case study was to build a **working prototype** that translates spoken English audio in a short video into one or more target languages, generates subtitles, and embeds them directly into the video.

---

## 2. Tool Selection

### Speech-to-Text
**Tool:** OpenAI Speech-to-Text API  
**Reason:**
- High transcription accuracy
- Minimal setup time
- Reliable for short-form video (15–30 seconds)

**Alternative considered:**
- Faster-Whisper (local, provides timestamps), I didn't use due to higher setup cost and local compute requirements

---

### Translation
**Tool:** OpenAI GPT (gpt-5-mini)  
**Reason:**
- Good balance between quality and cost
- Natural-sounding translations suitable for subtitles

---

### Video Processing
**Tool:** MoviePy + ffmpeg  
**Reason:**
- Python-native
- Easy subtitle compositing

---

## 3. Workflow

1. Extract audio from the input video
2. Transcribe English speech into text using OpenAI Speech-to-Text
3. Convert transcription into subtitle segments
4. Translate subtitles into target language(s) using GPT
5. Generate translated `.srt` files
6. Burn subtitles directly into the video using MoviePy
7. Export the final translated video

---

## 4. Results

### Quality Assessment
- Translation quality: Natural and understandable
- Subtitle synchronization: Acceptable for short clips
### Limitations
- Ambiguous sentences without visual context may be translated incorrectly  

---

## 5. Further improvements (Not Finished)

**Problem:** Subtitle translation can be inaccurate when context is ambiguous. For example, the English sentence “I love you” can be translated into Vietnamese as “Anh yêu em” or “Em yêu anh”, and this distinction cannot be determined without additional contextual information such as speaker identity or visual cues.

**Steps Attempted:** I attempted to extract video frames based on subtitle timestamps and pass these images to ChatGPT to provide additional visual context for translation. However, due to temporary errors from the OpenAI API at the time of testing, this approach could not be fully evaluated. Relevant commented code can be found in utils/translate.py. 

## 6. Time breakdown 

I spent approximately 15 minutes on research, followed by 2 hours and 15 minutes of implementation, and the final 30 minutes on writing documentation.

---

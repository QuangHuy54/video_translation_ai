# 🎥 AI-Powered Video Translation Tool

This project is a working prototype that translates spoken audio in a video into one or more target languages and burns translated subtitles directly into the video.

---

## ✨ Features

- Extract audio from video
- Transcribe English speech using OpenAI Speech-to-Text
- Translate subtitles into one or multiple languages
- Generate translated `.srt` files
- Burn subtitles directly into the output video.
- CLI-based usage (no UI)

---

### Python packages

```bash
pip install openai moviepy pysrt srt argparse python-dotenv 
```

### System dependencies

ffmpeg is required.

Please create the following directories before running the project: extracted_audio, extracted_frames, extracted_subtitles, output 

---

## 🔑 OpenAI API Setup

Set your OpenAI API key in .env file as in .env.example

---

## 🚀 How to Run

### Single language

```bash
python main.py --video_path input/sample_en.mp4 --language vietnamese
```

### Multiple languages

```bash
python main.py --video_path input/sample_en.mp4 --language vietnamese,japanese,french
```
---

## 📤 Output

For each target language:

Video with burned subtitles:
./output/sample_<language>.mp4

---
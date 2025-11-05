#!/usr/bin/env python3
"""
process_video.py
Simple CLI: extracts audio from an mp4 then transcribes with whisper.
Outputs:
 - transcript.vtt (webvtt captions)
"""

import sys
import os
import subprocess
import argparse
import tempfile
import whisper
from whisper import Whisper

def extract_audio(input_path, out_wav):
    # Use ffmpeg to produce a 16kHz mono wav (good for ASR)
    cmd = [
        "ffmpeg", "-y", "-i", input_path,
        "-ac", "1", "-ar", "16000",
        "-c:a", "pcm_s16le",
        out_wav
    ]
    subprocess.check_call(cmd)

def transcribe(model_name, wav_path, task="transcribe", language=None, output_prefix="transcript"):
    # load model
    print(f"Loading model: {model_name} ...")
    model = whisper.load_model(model_name)

    print(f"Transcribing {wav_path} ...")
    # model.transcribe returns dict with 'text' and 'segments'
    result = model.transcribe(wav_path, task=task, language=language)

    # Save plain text
    # txt_out = f"{output_prefix}.txt"
    # with open(txt_out, "w", encoding="utf-8") as f:
    #     f.write(result["text"].strip() + "\n")
    # print(f"Saved plain transcript -> {txt_out}")

    # Save VTT (using simple output)
    vtt_out = f"{output_prefix}.vtt"
    with open(vtt_out, "w", encoding="utf-8") as f:
        f.write("WEBVTT\n\n")
        for seg in result["segments"]:
            start = seg["start"]
            end = seg["end"]
            # simple timestamp formatting
            def fmt(t):
                h = int(t // 3600)
                m = int((t % 3600) // 60)
                s = int(t % 60)
                ms = int((t - int(t)) * 1000)
                return f"{h:02d}:{m:02d}:{s:02d}.{ms:03d}"
            f.write(f"{fmt(start)} --> {fmt(end)}\n")
            f.write(seg["text"].strip() + "\n\n")
    print(f"Saved fallback VTT -> {vtt_out}")

def main():
    parser = argparse.ArgumentParser(description="Transcribe mp4 locally using Whisper")
    parser.add_argument("input", help="input mp4 file path")
    parser.add_argument("--model", default="small", help="whisper model size (tiny, base, small, medium, large)")
    parser.add_argument("--language", default="en", help="optional: force language (e.g., 'en')")
    args = parser.parse_args()

    if not os.path.isfile(args.input):
        print("Input file not found:", args.input)
        sys.exit(2)

    with tempfile.TemporaryDirectory() as tmpdir:
        wav_path = os.path.join(tmpdir, "extracted.wav")
        print("Extracting audio to WAV...")
        extract_audio(args.input, wav_path)
        transcribe(args.model, wav_path, language=args.language, output_prefix=args.input)

if __name__ == "__main__":
    main()

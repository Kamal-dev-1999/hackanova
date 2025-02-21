import os
import whisper
import nltk
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import subprocess
from moviepy.editor import AudioFileClip


def MP4ToMP3(mp4):
    """Function to convert MP4 video to MP3 audio using moviepy."""
    try:
        # Generate output MP3 path
        mp3_path = os.path.splitext(mp4)[0] + ".mp3"

        # Convert MP4 to MP3
        with AudioFileClip(mp4) as audio_clip:
            audio_clip.write_audiofile(mp3_path)

        print(f"Audio extracted and saved to: {mp3_path}")
        return mp3_path

    except Exception as e:
        print(f"Error during MP4 conversion: {e}")
        return None


def process_audio(mp3_path):
    # Define the path for transcription
    output_path_transcription = os.path.splitext(mp3_path)[0] + ".txt"

    # Transcribe the MP3 file using Whisper
    model = whisper.load_model("base")
    result = model.transcribe(mp3_path)
    transcript = result["text"]
    transcript_words = len(transcript.split())

    # Save the transcription to a text file
    with open(output_path_transcription, 'w', encoding='utf-8') as file:
        file.write(transcript)

    # Summarize the transcription using HuggingFace's DistilBART model
    tokenizer = AutoTokenizer.from_pretrained("sshleifer/distilbart-cnn-12-6")
    model = AutoModelForSeq2SeqLM.from_pretrained("sshleifer/distilbart-cnn-12-6")

    # Tokenize and split transcript into chunks
    sentences = nltk.tokenize.sent_tokenize(transcript)
    length = 0
    chunk = ""
    chunks = []
    count = -1

    for sentence in sentences:
        count += 1
        combined_length = len(tokenizer.tokenize(sentence)) + length
        if combined_length <= tokenizer.model_max_length:
            chunk += sentence + " "
            length = combined_length
            if count == len(sentences) - 1:
                chunks.append(chunk.strip())
        else:
            chunks.append(chunk.strip())
            length = 0
            chunk = sentence + " "
            length = len(tokenizer.tokenize(sentence))

    # Generate summaries for each chunk
    inputs = [tokenizer(chunk, return_tensors="pt") for chunk in chunks]
    summary = []
    for input in inputs:
        output = model.generate(**input, max_length=int(len(input['input_ids'][0]) / 2), min_length=0)
        summary.append(tokenizer.decode(*output, skip_special_tokens=True))

    # Save the summary to a file
    output_path_summary = os.path.splitext(mp3_path)[0] + "_summary.txt"
    with open(output_path_summary, 'w', encoding='utf-8') as file:
        file.write("\n".join(summary))

    # Get audio duration using ffprobe
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1",
         mp3_path], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    duration = "%.2f" % (float(result.stdout) / 60) + " min"

    # Prepare the result data
    summary_text = "\n".join(summary)
    summary_words = len(summary_text.split())

    # Print the result (you can change this to save to a database or other storage if needed)
    print(f"Summary: {summary_text}")
    print(f"Summary Words: {summary_words}")
    print(f"Transcript Words: {transcript_words}")
    print(f"Duration: {duration}")


if __name__ == "__main__":
    # Path to the video file
    video_path = r"C:/Users/Kamal/Briefify/best.mp4"  # Update this path to your video

    # Convert MP4 to MP3 and get the MP3 path
    mp3_path = MP4ToMP3(video_path)

    if mp3_path:
        # Process the MP3 file after conversion
        process_audio(mp3_path)
    else:
        print("MP3 conversion failed. Exiting.")
import requests
import os

from youtube_transcript_api import YouTubeTranscriptApi


def download_caption(video_id, language_code):
    try:
        # Fetch the available transcripts for the video
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

        # Get the transcript for the specified language
        transcript = transcript_list.find_transcript([language_code])

        # Fetch the actual transcript data
        caption_data = transcript.fetch()

        # Convert the caption data to SRT format
        srt_data = convert_to_srt(caption_data)

        # Save the SRT data to a file
        filename = f"{video_id}_{language_code}.srt"
        with open(filename, "w", encoding="utf-8") as file:
            file.write(srt_data)
        print(f"Caption downloaded: {filename}")
    except Exception as e:
        print(f"Error downloading caption: {str(e)}")


def convert_to_srt(caption_data):
    srt_lines = []
    for i, caption in enumerate(caption_data, start=1):
        text = caption["text"].replace("\n", " ")
        srt_lines.append(f"{text}")
    return "\n".join(srt_lines)


# Usage example
video_id = "_w1vv7_dU2Y"
language_code = "en"  # Specify the language code for the desired caption language

download_caption(video_id, language_code)

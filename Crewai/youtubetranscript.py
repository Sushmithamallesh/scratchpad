# your_custom_script.py

from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import JSONFormatter

# Must be a single transcript.
video_id = "_w1vv7_dU2Y"
transcript = YouTubeTranscriptApi.get_transcript(video_id)

formatter = JSONFormatter()

# .format_transcript(transcript) turns the transcript into a JSON string.
json_formatted = formatter.format_transcript(transcript)


# Now we can write it out to a file. This will create the file if it doesn't exist.
with open("test.json", "w+", encoding="utf-8") as json_file:
    json_file.write(json_formatted)

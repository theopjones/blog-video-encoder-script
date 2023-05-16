import os
import subprocess
import random
import string

# Check if input file name is supplied
if len(os.sys.argv) != 2:
    print("Usage: python3 script.py <input_file>")
    os.sys.exit(1)

input_file = os.sys.argv[1]
bitrate_audio_144p = "32k"
bitrate_audio_240p = "64k"
bitrate_audio_360p = "128k"
bitrate_audio = "360k"

# Define a dictionary of output resolutions and video bitrates
resolutions = {
    "144p": "200k",
    "240p": "400k",
    "360p": "1M",
    "480p": "4M",
    "720p": "7.5M",
    "1080p": "12M",
}

host_url = input("Please enter the URL (without https) where the videos will be hosted:\n")

# Random string for unique IDs
rand_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))

buttons_line = ""

for resolution, bitrate_video in resolutions.items():
    output_file = f"{input_file.rsplit('.', 1)[0]}_{resolution}.mp4"

    # Set audio bitrate depending on the resolution
    bitrate_audio_current = bitrate_audio
    if resolution == "240p":
        bitrate_audio_current = bitrate_audio_240p
    elif resolution == "360p":
        bitrate_audio_current = bitrate_audio_360p
    elif resolution == "144p":
        bitrate_audio_current = bitrate_audio_144p

    command = [
        'ffmpeg', '-i', input_file, '-vf', f"scale=-2:{resolution[:-1]}", '-c:v',
        'libx264', '-b:v', bitrate_video, '-c:a', 'aac', '-b:a', bitrate_audio_current, output_file
    ]
    subprocess.run(command, check=True)

    # Add button to buttons line
    buttons_line += f'\n<button style="margin-right: 10px;" onclick="changeQuality{rand_str}(\'https://{host_url}/{output_file}\')">{resolution}</button>'

with open('videotemplate.html', 'r') as template_file:
    template_content = template_file.read()

# Replace placeholders in the template
html_content = template_content \
        .replace("RANDOM", rand_str) \
        .replace("BUTTONS_PLACEHOLDER", buttons_line) \
        .replace("DEFAULT_MOBILE_SOURCE", f"https://{host_url}/{input_file.rsplit('.', 1)[0]}_480p.mp4") \
        .replace("DEFAULT_DESKTOP_SOURCE", f"https://{host_url}/{input_file.rsplit('.', 1)[0]}_720p.mp4")

# Write the HTML content to a file
with open('videos.html', 'w') as output_file:
    output_file.write(html_content)
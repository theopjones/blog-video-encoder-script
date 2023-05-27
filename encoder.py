'''
Written in 2023 by Theodore Jones tjones2@fastmail.com 
To the extent possible under law, the author(s) have dedicated all copyright 
and related and neighboring rights to this software post to the public domain worldwide. 
This software is distributed without any warranty. 
http://creativecommons.org/publicdomain/zero/1.0/.
'''

import os
import concurrent.futures
import subprocess
import random
import string

# Check if input file name is supplied
if len(os.sys.argv) != 2:
    print("Usage: python3 script.py <input_file>")
    os.sys.exit(1)

def encode_video(resolution, bitrate_video, bitrate_audio_current):
    output_file = f"{input_file.rsplit('.', 1)[0]}_{resolution}.mp4"
    command = [
    'ffmpeg', '-i', input_file, '-vf', f"scale=-2:{resolution[:-1]}", '-c:v',
    'libx264', '-b:v', bitrate_video, '-c:a', 'aac', '-b:a', bitrate_audio_current, 
    '-movflags', '+faststart', output_file
    ]
    subprocess.run(command, check=True)

input_file = os.sys.argv[1]
bitrate_audio_144p = "32k"
bitrate_audio_240p = "64k"
bitrate_audio_360p = "128k"
bitrate_audio = "360k"

# Define a dictionary of output resolutions and video bitrates
resolutions = {
    "144p": "200k",
    "240p": "400k",
    "360p": "1.5M",
    "480p": "4M",
    "720p": "7.5M",
    "1080p": "12M",
    "2160p" : "68M"
}

with concurrent.futures.ProcessPoolExecutor() as executor:
    buttons_line_futures = {executor.submit(
        encode_video, resolution, bitrate_video,
        bitrate_audio_144p if resolution == "144p" else bitrate_audio_240p if resolution == "240p" else bitrate_audio_360p if resolution == "360p" else bitrate_audio
        ): resolution for resolution, bitrate_video in resolutions.items()}
    




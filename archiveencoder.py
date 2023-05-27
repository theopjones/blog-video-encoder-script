import os
import sys
import subprocess

# Get the input folder from command line arguments
if len(sys.argv) < 2:
    print('Usage: python encode_videos.py <input_folder>')
    sys.exit(1)

input_folder = sys.argv[1]
output_folder = os.path.join(input_folder, 'ArchiveEncoded')

# Create the output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Get a list of all files in the input folder
files = os.listdir(input_folder)

for file in files:
    # Only process video files (considering case sensitivity and more file types)
    if file.lower().endswith(('.mp4', '.mov', '.avi', '.mkv', '.flv', '.wmv')):

        # Full path to the original file
        original_file = os.path.join(input_folder, file)

        # Full path to the new file
        new_file = os.path.join(output_folder, file)

        # Get bitrate and resolution of the input video
        ffprobe_command = [
            'ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries',
            'stream=bit_rate,height', '-of', 'default=noprint_wrappers=1:nokey=1', original_file
        ]
        result = subprocess.run(ffprobe_command, text=True, capture_output=True)

        # Extract bitrate and resolution
        input_bitrate, input_height = map(int, result.stdout.strip().split('\n'))

        # Calculate output bitrate
        if input_height >= 1080:
            output_bitrate = min(20_000_000, int(input_bitrate * 0.5))
        elif input_height >= 720:
            output_bitrate = min(15_000_000, int(input_bitrate * 0.5))
        else:
            output_bitrate = min(7_500_000, int(input_bitrate * 0.5))

        # Construct the ffmpeg command
        command = [
            'ffmpeg', '-i', original_file,
            '-vf', 'scale=-1:min(ih\,1080)',
            '-c:v', 'libx264', '-crf', '23',
            '-strict', '-2',
            '-c:a', 'aac', '-b:a', '320k',
            new_file
            ]

        # Run the command
        subprocess.run(command)

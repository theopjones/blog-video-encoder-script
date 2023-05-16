This repo contains scripts to quickly encode video and prepare HTML snippets for self-hosting videos on a blog. By using the `encoder.py` script, based on an input video you can produce a set of encoded video files playable by the great majority of current browsers at multiple resolutions (1080p, 720p, 480p, 360p, 240p, 144p) along with a corresponding HTML snippet which can be used on a website to allow the user of that website to play the video. 

This only requires a HTTPS server which stores the files, it does not use a video hosting platform. This code is useful for self-hosting video files if you do not want to use a service like Youtube/Vimeo/Odyssey/etc to host a collection of long form video content for your blog or personal website, but you find full-featured self-hosted video platforms like Peertube/LBRY/MediaCMS/etc too bulky and heavy weight for your needs. 

# videotemplate.html

The `videotemplate.html` file contains a template (HTML/Javascript/CSS) for a video player widget which is filled out by the `encoder.py` file. The completed HTML code can then be added to anouther website, or the HTML editor of a blogging engine. 

This template uses the HTML5 video attribute to play a video. Controls are enabled. The code supports the option for multiple resolutions, and allows switching between the resolutions. The Javascript controling this is able to detect if the user is running on a mobile browser. There is the ability to set a different default resolution   

The `<video>` object will autoscale based on the size of the container that it is in, but this will not cause the resolution of the video to change without user intervention. 

A screenshot of this widget is as follows. 

![](Screenshot_2023-05-16_14-58-52.png)

# encoder.py 

The command line usage of this script is as follows `python3 script.py <input_file>`

The script will also prompt for the URL (without https) where the videos will be hosted. This should be a domain name + a path (if needed) ie. `videofiles.example.com/VideoFilePath`. Once the encoding is complete, use your prefered method to upload the encoded files to the HTTPS server in the correct path. 

FFmpeg needs to be installed, but any any corresponding python library. Otherwise, this script's only dependencies are in the Python standard library. 

This python script writes the following two items to the current working directory 

1. A set of encoded video files corresponding to the following resolutions 1080p, 720p, 480p, 360p, 240p, 144p
2. A file named `videos.html` which containes a HTML file based on `videotemplate.html` which allows all of those encoded video files to be played in a browser.

The output video files are in MP4 with H.264 and AAC.

The `videos.html` file is set up to default to 480p for mobile browsers, and 720p video for all other browsers. 

A mobile browser is any browser for which `navigator.userAgent` in Javascript contains any of the following strings `iPhone`, `iPad`, `iPod`, `Android`. 

The name of JS functions, and HTML IDs is randomized in order to make it possible for multiple copies of the code to exist on the same web page (ie. for something like a blog homepage).

The bit rates of the encoded video files are as follows

|       | Video   | Audio   |
|-------|---------|---------|
| 144p  | 200kbps | 32kbps  |
| 240p  | 400kbps | 64kbps  |
| 360p  | 1mbps   | 128kbps |
| 480p  | 4mbps   | 360kbps |
| 720p  | 7.5mbps | 360kbps |
| 1080p | 12mbps  | 360kbps |


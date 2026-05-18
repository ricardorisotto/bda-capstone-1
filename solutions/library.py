from pathlib import Path
import yt_dlp

# A function that downloads a video from a given URL
def download_video(url):
    # download one video
    Path("videos").mkdir(exist_ok=True)

    # Save inside videos/ using the video title as the filename
    ydl_options = {
        "outtmpl": "videos/%(title)s.%(ext)s"
    }

    with yt_dlp.YoutubeDL(ydl_options) as ydl:
        ydl.download([url])

# a function that reads the URLs from the CSV file
# it skips the header and returns a list of URLs
# the CSV file is expected to have "title, URL" per line, with a header line at the top
# so we skip the first line and read the second column of each subsequent line as the URL   
def read_urls_from_csv(filename):
    urls = []
    with open(filename, "r") as f:
        next(f)  # Skip the header line
        for line in f:
            # Get the URL from the second column (after the comma)
            url = line.strip().split(",")[1]
            urls.append(url)
    return urls
from pathlib import Path
import yt_dlp

# A function that downloads a video from a given URL
def download_video(url):
    # download one video
    Path("videos").mkdir(exist_ok=True)

    # Save inside videos/ using the video title as the filename
    ydl_options = {
        "outtmpl": "videos/%(title)s.%(ext)s",
        "socket_timeout": 30,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_options) as ydl:
            ydl.download([url])
        
        return {
            "url": url,
            "status": "success",
            "error": "",
        }
    except Exception as e:
        print(f"Error downloading {url}: {e}")
        return {
            "url": url,
            "status": "failed",
            "error": str(e),
        }

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

# A funtion that downloads video metadata from a given URL.
# The metadata should include the following: 
# {
#    "title": "...",
#    "duration": 10,
#    "uploader": "...",
#    "view_count": 12345,
#    "ext": "mp4",
#    "url": "..."
# }
def get_video_metadata(url):
    ydl_options = {
        "quiet": True,
        "skip_download": True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_options) as ydl:
            info = ydl.extract_info(url, download=False)
            metadata = {
                "title": info.get("title"),
                "duration": info.get("duration"),
                "uploader": info.get("uploader"),
                "view_count": info.get("view_count"),
                "ext": info.get("ext"),
                "url": url
            }
            return metadata
    except Exception as e:
        print(f"Error extracting metadata for {url}: {e}")
        return {
            "title": "N/A",
            "duration": None,
            "uploader": "N/A",
            "view_count": None,
            "ext": "N/A",
            "url": url
        }

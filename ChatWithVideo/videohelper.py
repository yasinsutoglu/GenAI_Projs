# scrapetube, yt_dlp,pydub => youtube related libs
# VIDEO => SOUNDS => SCRIPTS process file
import scrapetube
import os
from dotenv import load_dotenv
from youtubevideo import YoutubeVideo # our custom class
# These Below Loaders => Abstracted LangChain Classes; finds related videos -> downloads media files -> extracts sound file ->
# converts to transcript via whisper
from langchain_community.document_loaders.generic import GenericLoader # "middleware class" that is used in parsing jobs
from langchain_community.document_loaders import YoutubeAudioLoader
from langchain_community.document_loaders.parsers import OpenAIWhisperParser


load_dotenv()

my_key_openai = os.getenv("openai_apikey")

#1-Transcription Function
def get_video_transcript(url):
    target_dir = "./audios/"

    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    
    loader = GenericLoader(
        YoutubeAudioLoader(urls=[url], save_dir=target_dir),
        OpenAIWhisperParser(api_key=my_key_openai)
    )

    video_transcript_docs = loader.load() # returns List[Document]

    return video_transcript_docs

#2 Youtube Search Function
def get_videos_for_search_term(search_script, video_count=1, sorting_criteria="relevance"):
    convert_sorting_option = {
                                "Most Related": "relevance",
                                "By UploadDate": "upload_date",
                                "By ViewCount": "view_count",
                                "By Rating": "rating"
                            }

    videos = scrapetube.get_search(query=search_script, limit=video_count, sort_by=convert_sorting_option[sorting_criteria])
    videolist = list(videos)
    
    youtube_videos = [] # shall be class list

    for video in videolist:
        new_video = YoutubeVideo(
            video_id = video["videoId"],
            video_title=video["title"]["runs"][0]["text"],
            video_url = "https://www.youtube.com/watch?v=" + video["videoId"],
            channel_name= video["longBylineText"]["runs"][0]["text"],
            duration= video["lengthText"]["accessibility"]["accessibilityData"]["label"],
            publish_date = video["publishedTimeText"]["simpleText"]
        )

        youtube_videos.append(new_video)

    return youtube_videos


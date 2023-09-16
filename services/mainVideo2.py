from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip,ImageClip,AudioFileClip
# Load your video clip
import requests
import base64
# import io
# import tempfile
from pydub import AudioSegment
import zlib

def video():
    
    # Audio file 
    url='https://775b-2409-40d0-100c-3df-3ed5-44bc-fe8b-2a8.ngrok-free.app/text_to_audio'
    data={
      "count": 1,
      "texts": [
        {
          "text": "this is abhishek",
          "voice_gender": "Male"
        }
      ]
    }
    headers={
        'Content-Type': 'application/json',
        'ngrok-skip-browser-warning': 'huehuehue',
    }
    response=requests.post(url,json=data,headers=headers)
    if response:
    
        audio_data = response.json()["audio"][0]["data"]
        duration=  response.json()["audio"][0]["duration"]

        audio_bytes = base64.b64decode(audio_data)
        decompressed_audio = zlib.decompress(audio_bytes)
        with open("audio.mp3", "wb") as f:
            f.write(decompressed_audio)

    else:
        print("error",response)
    video_clip = VideoFileClip("finalBackground.mp4").set_duration(5)
    # Image file
    # image=ImageClip("https://upload.wikimedia.org/wikipedia/commons/1/1d/Football_Pallo_valmiina-cropped.jpg")
    image=ImageClip("75_logo.png")
    extraImages=ImageClip('PMmodi.png')

    audio=AudioFileClip('audio.mp3').set_duration(duration)
    print(audio,'audio')

    video_clip=video_clip.set_audio(audio)
    video_width, video_height = video_clip.size
    text_width, text_height = image.size
    top_right_x = video_width - text_width
    top_right_y = 0  # Position at the top
    
    extraImages=extraImages.set_position(('right','center')).set_duration(5)
    image=image.set_position((top_right_x,top_right_y)).set_duration(5)


    # Create an array of text clips

    heading=TextClip("Heading from the house of Prime minister",fontsize=30,color='black',bg_color='gray').set_position(('left','top')).set_duration(5)

    text_clips = []

    # Define text content, duration, and position for each text clip
    text_data = [
        {"text": """ 
         Lorem ipsum dolor sit amet consectetur adipisicing elit. Ipsam aliquid dolorem blanditiis non ipsum perferendis enim.
          Lorem ipsum dolor sit amet consectetur adipisicing elit. Ipsam aliquid dolorem blanditiis non ipsum perferendis enim.
          Lorem ipsum dolor sit amet consectetur adipisicing elit. Ipsam aliquid dolorem blanditiis non ipsum perferendis enim.
          Lorem ipsum dolor sit amet consectetur adipisicing elit. Ipsam aliquid dolorem blanditiis non ipsum perferendis enim.
          Lorem ipsum dolor sit amet consectetur adipisicing elit. Ipsam aliquid dolorem blanditiis non ipsum perferendis enim.
          Lorem ipsum dolor sit amet consectetur adipisicing elit. Ipsam aliquid dolorem blanditiis non ipsum perferendis enim.
          Lorem ipsum dolor sit amet consectetur adipisicing elit. Ipsam aliquid dolorem blanditiis non ipsum perferendis enim.
          Lorem ipsum dolor sit amet consectetur adipisicing elit. Ipsam aliquid dolorem blanditiis non ipsum perferendis enim.
          Lorem ipsum dolor sit amet consectetur adipisicing elit. Ipsam aliquid dolorem blanditiis non ipsum perferendis enim.
          Lorem ipsum dolor sit amet consectetur adipisicing elit. Ipsam aliquid dolorem blanditiis non ipsum perferendis enim.
          Lorem ipsum dolor sit amet consectetur adipisicing elit. Ipsam aliquid dolorem blanditiis non ipsum perferendis enim.
          Lorem ipsum dolor sit amet consectetur adipisicing elit. Ipsam aliquid dolorem blanditiis non ipsum perferendis enim.
          Lorem ipsum dolor sit amet consectetur adipisicing elit. Ipsam aliquid dolorem blanditiis non ipsum perferendis enim.""", "duration": 5, "position": ("left","center")},
        {"text": "Text 2", "duration": 5, "position": (0.5,0.5)},
        # Add more text clips as needed
    ]

    # Create and append TextClip objects to the array
    start=0
    for data in text_data:
        text_clip = TextClip(data["text"], fontsize=25, color='black')
        text_clip=text_clip.set_start(start,change_end=True)
        start=start+data["duration"]
        text_clip = text_clip.set_duration(data["duration"])
        text_clip = text_clip.set_position(data["position"])
        text_clips.append(text_clip)

    # Composite the text clips onto the video clip
    video_with_text = CompositeVideoClip([video_clip,image,extraImages,heading] + text_clips)

    # Write the final video to a file
    video_with_text.write_videofile("output_video.mp4")

video()

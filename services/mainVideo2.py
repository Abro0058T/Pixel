from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip,ImageClip,AudioFileClip
# Load your video clip
import requests
import base64
# import io
# import tempfile
import cloudinary
import cloudinary.uploader
import cloudinary.api
from tempCodeRunnerFile import get_release

cloudinary.config(
    cloud_name="dsztz2gsf",
    api_key="661837983169221",
    api_secret="58BTwHOeZPJ8yit4XbTJ9CtYw4w"
)



from pydub import AudioSegment
import zlib

def video(images,texts):
    
    # Audio file 
    audio_text=[]
    final_text=""
    azure_final_text=""
    for text in texts:
  
        final_text+=text["text"]+"\t"+"\n"
        azure_final_text+=text["azure_text"]
        audio_text.append({"text":text["azure_text"],"voice_gender":"Female"})
    # print(audio_text)'
    audio_text.append({"text":azure_final_text,"voice_gender":"Female"})
    # print(final_text)
    url='https://8baf-2409-40d0-be-9fee-7d9a-3ad4-6a37-fcd6.ngrok-free.app/text_to_audio'
    data={
      "count": 1,
      # "texts": [
      #   {
      #     "text": final_text,
      #     "voice_gender": "Female",
      #   }
      # ]
      "texts":audio_text
    }
    headers={
        'Content-Type': 'application/json',
        'ngrok-skip-browser-warning': 'huehuehue',
    }
    response=requests.post(url,json=data,headers=headers)
    if response:
        audio_data = response.json()["audio"][len(audio_text)-1]["data"]
        duration=  response.json()["audio"][len(audio_text)-1]["duration"]


        audio_bytes = base64.b64decode(audio_data)
        decompressed_audio = zlib.decompress(audio_bytes)
        with open("audio.mp3", "wb") as f:
            f.write(decompressed_audio)

    else:
        print("error",response)
        exit()
    net_time=0
    for audio in response.json()["audio"][:-1]:
        net_time+=audio["duration"]
    video_clip = VideoFileClip("finalBackground.mp4").set_duration(duration)
    # Image file
    # image=ImageClip("https://upload.wikimedia.org/wikipedia/commons/1/1d/Football_Pallo_valmiina-cropped.jpg")
    if len(images)!=0:
        length_of_image=duration/(len(images))
        image_frames=[]
        image_duration=0
        # audio_count_image=0
        for image in images:
            image=ImageClip(image).resize((700,500)).set_position(('right','center')).set_start(image_duration).set_duration(length_of_image)
            image_duration+=length_of_image
            # audio_count_image+=1
            image_frames.append(image)
    
    image=ImageClip("75_logo.png")
    # extraImages=ImageClip('PMmodi.png')

    audio=AudioFileClip('audio.mp3').set_duration(duration)
    print(audio,'audio')

    video_clip=video_clip.set_audio(audio)
    video_width, video_height = video_clip.size
    text_width, text_height = image.size
    top_right_x = video_width - text_width
    top_right_y = 0  # Position at the top
    print("working1")
    # extraImages=extraImages.set_position(('right','center')).set_duration(5)
    image=image.set_position((top_right_x,top_right_y)).set_duration(duration)
    print("working2")

    # Create an array of text clips

    heading=TextClip("Heading from the house of Prime minister",fontsize=60,color='red',bg_color='rgb(238, 231, 233)').set_position(('left','top')).set_duration(net_time).margin(left=10,top=10)

    text_clips = []
    print("working3")
    # Define text content, duration, and position for each text clip
    # text_data = [
    #     {"text": """ 
    #      Lorem ipsum dolor sit amet consectetur adipisicing elit. Ipsam aliquid dolorem blanditiis non ipsum perferendis enim.
    #       Lorem ipsum dolor sit amet consectetur adipisicing elit. Ipsam aliquid dolorem blanditiis non ipsum perferendis enim.
    #       Lorem ipsum dolor sit amet consectetur adipisicing elit. Ipsam aliquid dolorem blanditiis non ipsum perferendis enim.
    #       Lorem ipsum dolor sit amet consectetur adipisicing elit. Ipsam aliquid dolorem blanditiis non ipsum perferendis enim.
    #       Lorem ipsum dolor sit amet consectetur adipisicing elit. Ipsam aliquid dolorem blanditiis non ipsum perferendis enim.
    #       Lorem ipsum dolor sit amet consectetur adipisicing elit. Ipsam aliquid dolorem blanditiis non ipsum perferendis enim.
    #       Lorem ipsum dolor sit amet consectetur adipisicing elit. Ipsam aliquid dolorem blanditiis non ipsum perferendis enim.
    #       Lorem ipsum dolor sit amet consectetur adipisicing elit. Ipsam aliquid dolorem blanditiis non ipsum perferendis enim.
    #       Lorem ipsum dolor sit amet consectetur adipisicing elit. Ipsam aliquid dolorem blanditiis non ipsum perferendis enim.
    #       Lorem ipsum dolor sit amet consectetur adipisicing elit. Ipsam aliquid dolorem blanditiis non ipsum perferendis enim.
    #       Lorem ipsum dolor sit amet consectetur adipisicing elit. Ipsam aliquid dolorem blanditiis non ipsum perferendis enim.
    #       Lorem ipsum dolor sit amet consectetur adipisicing elit. Ipsam aliquid dolorem blanditiis non ipsum perferendis enim.
    #       Lorem ipsum dolor sit amet consectetur adipisicing elit. Ipsam aliquid dolorem blanditiis non ipsum perferendis enim.""", "duration": 5, "position": ("left","center")},
    #     {"text": "Text 2", "duration": 5, "position": (0.5,0.5)},
    #     # Add more text clips as needed
    # ]

    # Create and append TextClip objects to the array
    start=0
    audio_count=0
    print("working4")
    for data in texts:
        print(data)
        text_clip = TextClip(data['text'], fontsize=30, color='red')
        text_clip=text_clip.set_start(start,change_end=True)
        start=start+response.json()["audio"][audio_count]["duration"]
        print("working5")
        text_clip = text_clip.set_duration(response.json()["audio"][audio_count]["duration"])
        print("working6")
        audio_count+=1
        text_clip = text_clip.set_position(data["position"])
        text_clips.append(text_clip)
    # Composite the text clips onto the video clip
    if len(images)!=0:
        video_with_text = CompositeVideoClip([video_clip,image,heading] + text_clips+image_frames)
    else:
        video_with_text = CompositeVideoClip([video_clip,image,heading] + text_clips)



    # Write the final video to a file
    video_with_text.write_videofile("output_video.mp4")
    upload_result=cloudinary.uploader.upload("output_video.mp4",resource_type="video")
    print("Video uploaded to Cloudinary:", upload_result["secure_url"])
    return url
    # print("working5")
image=["https://tse3.mm.bing.net/th?id=OIP.Vt3kGu4X6WQlmH91GpJpzgHaFH&pid=Api&P=0&h=180","https://tse1.mm.bing.net/th?id=OIP.1YM53mG10H_U25iPjop83QHaEo&pid=Api&P=0&h=180"]
text=[
      {"text": "The Vice President, Shri Jagdeep Dhankhar today emphasized the need to promote\nIndia’s glorious cultural heritage of India, spanning over 5000 years. He called upon the  \n media to recognize our cultural heritage and expressed the need to protect, support and \n nurture our artists in a structured manner.","azure_text": "The Vice President, Shri Jagdeep Dhankhar today emphasized the need to promote India’s glorious cultural heritage of India, spanning over 5000 years. He called upon the  media to recognize our cultural heritage and expressed the need to protect, support and  nurture our artists in a structured manner.", "duration": 5, "position": ('left','center')},
      # {"text": """Addressing a gathering after conferring the Sangeet Natak Akademi Amrit Awards\n at Vigyan Bhawan, in New Delhi today, the Vice President expressed his happiness in \n honoring the individuals whose contributions uphold the cultural heritage and pride of\n the nation.""", "duration": 5, "position": ('left','center')},
      {"text":  """Addressing a gathering after conferring the Sangeet Natak Akademi Amrit Awards\nat Vigyan Bhawan, in New Delhi today, the Vice President expressed his happiness in \nhonoring the individuals whose contributions uphold the cultural heritage and pride of\n  the nation.""","azure_text":  """Addressing a gathering after conferring the Sangeet Natak Akademi Amrit Awards at Vigyan Bhawan, in New Delhi today, the Vice President expressed his happiness in honoring the individuals whose contributions uphold the cultural heritage and pride of the nation.""", "duration": 5, "position": (0.5,0.5)},
]

def convertData(id):
    relese_data=get_release(id)
    texts=[]
    print(relese_data["paragraph"])
    def add_newline_every_n_words(text, n):
        # Split the text into words
        words = text.split()

        # Check if there are more than n words
        if len(words) <= n:
            return text

        # Create a list to hold lines of text with n words each
        lines = []
        for i in range(0, len(words), n):
            line = " ".join(words[i:i + n])
            lines.append(line)

        # Join the lines with newline characters
        result = "\n".join(lines)

        return result

    # Example usage:
    for text in relese_data["paragraph"]:
        azure_text=text.replace("\n", "").replace("\r", "")
        output_text = add_newline_every_n_words(text, 14)
        texts.append({'text':output_text,"azure_text":azure_text, "position": ('left','center')})

    images=[]
    for image in relese_data['imageList']:
        images.append(image)
    return (images,texts)

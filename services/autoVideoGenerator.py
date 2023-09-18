
# Importing libraries
import time
import hashlib
from urllib.request import urlopen, Request
from tempCodeRunnerFile import get_latest_release_id,get_release
from mainVideo2 import generate_video_task,convertData
import pymongo
from datetime import datetime

client = pymongo.MongoClient("mongodb://localhost:27017/")

db=client['pixel']

collection=db['videos']
# setting the URL you want to monitor


def detect():
	url = Request('https://benevolent-belekoy-1387de.netlify.app',
				headers={'User-Agent': 'Mozilla/5.0'})
	# to perform a GET request and load the
	# content of the website and store it in a var
	response = urlopen(url).read()
	# to create the initial hash
	currentHash = hashlib.sha224(response).hexdigest()
	print("running")
	time.sleep(10)
	while True:
		try:
			# perform the get request and store it in a var
			response = urlopen(url).read()
			# create a hash
			currentHash = hashlib.sha224(response).hexdigest()
			# wait for 30 seconds
			time.sleep(30)
			# perform the get request
			response = urlopen(url).read()
			# create a new hash
			newHash = hashlib.sha224(response).hexdigest()
			# check if new hash is same as the previous hash
			if newHash == currentHash:
				continue
			
			# if something changed in the hashes
			else:
				# notify
				print("something changed")
				latest_release_id=get_latest_release_id() # get latest notice prid
				addData(latest_release_id)
				converted_data=convertData(latest_release_id) #get latest notice data and convert it into required format 
				images,texts=converted_data
				video_data=generate_video_task(images,texts, latest_release_id) #convert to video and upload to cloudnary returns the url 
				addVideo(video_data,converted_data,latest_release_id)  # add video to mongodb data base
				# again read the website
				response = urlopen(url).read()
				# create a hash
				currentHash = hashlib.sha224(response).hexdigest()
				# wait for 600 seconds
				time.sleep(600)
				continue
			
		# To handle exceptions
		except Exception as e:
			print("error")

detect()
def addVideo(video_data,converted_data,latest_release_id):# runs only  when new notice is uploaded
	notice_data=get_release(latest_release_id)

	data={
		'prid':latest_release_id,
		'status':'waiting',
		'url':video_data,#cloudnaty url
		"user_email":"",
		"datetime":datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
		"ministry_name":"",
		"heading":"",
		"images":converted_data[0],
		"text_list":converted_data[1],
		"languages":notice_data["releaseLanguage"]
	}
	# finally update the video data with the given prid
	result=collection.update_one({"prid":latest_release_id},{"$set":data})

def addData(latest_release_id):
	data={
		"prid":latest_release_id,
	}
	# insert video data so that it status can be changed during video generation
	result=collection.insert_one(data)
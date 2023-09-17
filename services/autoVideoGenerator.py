
# Importing libraries
import time
import hashlib
from urllib.request import urlopen, Request
from tempCodeRunnerFile import get_latest_release_id,get_release
from mainVideo2 import video,convertData
import pymongo

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
				latest_release_id=get_latest_release_id()
				converted_data=convertData(latest_release_id)
				images,texts=converted_data
				video_data=video(images,texts)
				addVideo(video_data)
				# again read the website
				response = urlopen(url).read()
				# create a hash
				currentHash = hashlib.sha224(response).hexdigest()
				# wait for 30 seconds
				time.sleep(30)
				continue
			
		# To handle exceptions
		except Exception as e:
			print("error")

detect()
def addVideo(video_data):
	data={
		'prid':video_data["release_id"],
		'status':'waiting',
		'url':video_data['pageURL'],
		"user_email":"",
		"datetime":"date time ",
		"ministry_name":"",
		"heading":"",
		"images":video_data["imageList"],
		"text_list":video_data["paragraph"],
		"languages":video_data["releaseLanguage"]
	}
	result=collection.insert_one(data)
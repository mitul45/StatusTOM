import urllib2				# import library to do http requests
import serial				# import pyserial Library
import time				# import time library for delays
from multiprocessing import Process	# using multiprocessing instead of threading because we can stop process and not threads!
from xml.dom.minidom import parseString	# import xml parser called minidom
import subprocess			# a subprocess to send tweet when someone presses switch
import datetime


def twitterDisplay():

	# as this function will be called by new subprocess recreate the connection.
	serialPort = '/dev/ttyACM0'			# on ubuntu it uses either of this two.
	#serialPort = '/dev/ttyACM1'
	baudRate = 9600					# set transmission rate = 9600 bits/sec
	ser = serial.Serial(serialPort, baudRate)	# lets make a connection.
#	time.sleep(5)					# wait till connection gets stable.
	
#	twitterUserName = raw_input("Enter Twitter username to display tweets from : ")	# ask user name
	twitterUserName = 'mitul_45'
	URL = 'https://api.twitter.com/1/statuses/user_timeline.rss?screen_name=' + twitterUserName
	offset = 1								# from where the actual data starts in corrosponding URLs.

	firstTime = True
	lastRefreshed = time.time()
	while True:									# run for infinatiy and beyond
		if ((time.time() - lastRefreshed >= 300) or (firstTime)):		# fetch new data every 5 mins = 60*5 = 300secs.
     			lastRefreshed = time.time()
			file = urllib2.urlopen(URL)					# get the contents.
			data = file.read()						# convert to string
			file.close()							# close the file
			localOffset = offset
			firstTime = False
 	
		dom = parseString(data)							# parse the xml from the string
		xmlTag = dom.getElementsByTagName('title')[localOffset].toxml("utf-8")	# retrive the data with tag named 'title'
		localOffset += 1							# an offset
		xmlData=xmlTag.replace('<title>','').replace('</title>','')		# strip off the tag (<tag>data</tag>  --->   data)
		
		ser.write('^')			# a marker to indicate name of URL - to dispaly it on first line of Screen.
		ser.write('  Notification')	# display name
		ser.write('^')			# end of title.
				
		ser.write('~')	     		# write the marker ~ to serial to indicate start of data.
		words = xmlData.split(' ')	# split the string into individual words
		for word in words:		# loop until all words in string have been printed
			ser.write(word)		# write one word
  			ser.write(' ')		# than the space
  			time.sleep(2)		# THE DELAY IS NECESSARY. It prevents overflow of the arduino buffer.
		ser.write('~')			# write ~ to close the string and tell arduino information sending is finished
		time.sleep(2)			# let the user read the contents.

def display(n):

	serialPort = '/dev/ttyACM0'			# on ubuntu it uses either of this two.
	#serialPort = '/dev/ttyACM1'
	baudRate = 9600				# set transmission rate = 9600 bits/sec
	ser = serial.Serial(serialPort, baudRate)	# lets make a connection.

	URLs = ['http://rss.cnn.com/rss/edition_world.rss',
		'https://api.twitter.com/1/statuses/user_timeline.rss?screen_name=timesofindia',
		'https://news.google.com/news/feeds?pz=1&cf=all&ned=in&hl=en&output=rss',
		'http://news.yahoo.com/rss/asia',
		'http://ibnlive.in.com/ibnrss/rss/business/business.xml',
		'http://www.firstpost.com/india/feed',
		'http://www.firstpost.com/tech/feed']					# list of URLs to fetch data from.
	names = ['  CNN - World',' TOI - Twitter',' Google - India',' Yahoo! - Asia','IBN - Business',' Fistpost-India',' Firstpost-Tech']
	offset = [2,1,2,2,2,1,1]			# from where the actual data starts in corrosponding URLs.
	time.sleep(5)					# wait till connection gets stable.
	firstTime = True
	lastRefreshed = time.time()
	URLno = n
	while True:									# run for infinatiy and beyond!
		if ((time.time() - lastRefreshed >= 300) or (firstTime)):		# fetch new data every 5 mins = 60*5 = 300secs.
     			lastRefreshed = time.time()
			file = urllib2.urlopen(URLs[URLno])				# get the contents.
			data = file.read()						# convert to string
			file.close()							# close the file
			localOffset = offset[URLno]
			firstTime = False
 	
		dom = parseString(data)							# parse the xml from the string
		xmlTag = dom.getElementsByTagName('title')[localOffset].toxml("utf-8")	# retrive the data with tag named 'title'
		localOffset += 1							# an offset
		xmlData=xmlTag.replace('<title>','').replace('</title>','')		# strip off the tag (<tag>data</tag>  --->   data)
		
		ser.write('^')		# a marker to indicate name of URL - to dispaly it on first line of Screen.
		ser.write(names[URLno])	# display name
		ser.write('^')		# end of title.
				
		ser.write('~')	     		# write the marker ~ to serial to indicate start of data.
		words = xmlData.split(' ')	# split the string into individual words
		for word in words:		# loop until all words in string have been printed
			ser.write(word)		# write one word
  			ser.write(' ')		# than the space
  			time.sleep(2)		# THE DELAY IS NECESSARY. It prevents overflow of the arduino buffer.
		ser.write('~')			# write ~ to close the string and tell arduino information sending is finished
		time.sleep(2)			# let the user read the contents.


# start main
# print a welcome message and provide options to choose

print "==>> A Smart Display System built on Arduino and Python as backend <<=="
choice = raw_input(" Where you want to place this system?\n    1. At Door to display notification when you are not in office\n    2. On your table to display latest news and some follow other sites\n    3. To send a notice to every screen connected to system\n Enter Choice (1/2/3) : ")

# start a serial connection to talk to arduino

serialPort = '/dev/ttyACM0'			# on ubuntu it uses either of this two.
#serialPort = '/dev/ttyACM1'
baudRate = 9600					# set transmission rate = 9600 bits/sec
ser = serial.Serial(serialPort, baudRate)	# lets make a connection.
time.sleep(5)					# wait till connection gets stable.

# broadcast a message
if(choice == '3'):
	
	# take input message to be broadcasted
	broadcastMessage = raw_input("Enter message to be broadcasted : ")
	while True:									
		ser.write('^')				# a marker to indicate title to dispaly on first line of Screen.
		ser.write('     Notice')
		ser.write('^')		
						
		ser.write('~')	     			# write the marker ~ to serial to indicate start of data.
		words = broadcastMessage.split(' ')	# split the string into individual words
		for word in words:			# loop until all words in string have been printed
			ser.write(word)			# write one word
  			ser.write(' ')			# than the space
  			time.sleep(2)			# THE DELAY IS NECESSARY. It prevents overflow of the arduino buffer.
		ser.write('~')				# write ~ to close the string and tell arduino information sending is finished
		time.sleep(2)				# let the user read the contents.

elif(choice == '1'):
	
	p = Process (target = twitterDisplay)	# start the displaying values.
	p.start()				# start the process!

	print 'Press button to tweet back to sir to inform that you are waiting for him.'
	# keep waiting for serial input for informing back the user and call subprocess to display tweets.
	
	while 1:
		n = ser.read()
		while(n == 0):							# untill there is no data i.e. button is not pressed.
			n = ser.read()
			pass
		
		print 'button pressed!'
		
		#while((ser.read() == '1') or (ser.read() == '2')):		# due to debouncing wait for more than one '1's
		#	pass
		
		now = datetime.datetime.now()
		
		print 'Sending tweet.'
		msg = 'Sir, Some one is waiting at office. Time : ' + str(now.hour) + '.' + str(now.minute) + ' @mitul_45'		# create a tweet
		command = 'twitter -emitul_45@yahoo.co.in set %s' % msg		# tweet!
		subprocess.call(command, shell=True)

elif(choice == '2'):

	totalThreads = 7
	thread = 4
	p = Process(target = display,args = (thread,))	# start the displaying values with default first argument.
	p.start()					# start the process!
	
	print 'Press left button to go to previous feed and right button to go to next feed.'
	
	while 1:
		n = ser.read()
		while(n == 0):
			n = ser.read()
			pass
		if(n == '1'):
			while(ser.read() == '1'):
				pass
			thread -= 1				# left button pressed.
			if (thread == -1):
				thread = totalThreads - 1;
			else:				
				thread = thread % totalThreads
		elif(n == '2'):
			while(ser.read() == '2'):
				pass
			thread += 1				# right button pressed.
			thread = thread % totalThreads
	
		p.terminate()					# change the URL
	
		print thread
		p = Process(target = display,args = (thread,))
		p.start()						# fire it!!

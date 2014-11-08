import urllib2
import json
import time
import subprocess


while True:
	try:
		print "Request going out ..."
		response = urllib2.urlopen('http://shmooph.com:5000/flag')
		if response.getcode() == 200:
			print "Response received."
			data = json.load(response)
			print data
			if data['flag']:
				subprocess.call(['./superman.sh'])
	except urllib2.URLError,e:
		print e
		print e.reason
	time.sleep(1)

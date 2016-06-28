from googlevoice import Voice,util
from time import sleep
import urllib2
import json
import os
import uuid

voice = Voice()

try:
	with open('obfuscateMe.txt', 'r') as obfuscateMe:
		for lineA in obfuscateMe:
			NeedsEncryption = lineA
    
	with open('obfuscateEncryptionMe.txt', 'r') as obEncryptionMe:
		for lineB in obEncryptionMe:
			NeedsMoreEncryption = lineB
    
	with open('SendTo.txt', 'r') as sendToNumba:
		for lineC in sendToNumba:
			sendTo = lineC
	with open('APIKey.txt', 'r') as APIKeyText:
		for lineD in APIKeyText:
			APIKey = lineD

finally:
	obfuscateMe.close()
	obEncryptionMe.close()
	sendToNumba.close()

def getTemp():
	f = urllib2.urlopen('http://api.wunderground.com/api/'+ lineD +'/geolookup/conditions/q/MN/Minneapolis.json')
	json_string = f.read()
	parsed_json = json.loads(json_string)
	location = parsed_json['location']['city']
	temp_f = parsed_json['current_observation']['temp_f']
	condish = parsed_json['current_observation']['relative_humidity']
	weather = parsed_json['current_observation']['weather']
	return "%s:\nTemp: %s*F\nHumidity: %s\nWeather: %s" % (location, temp_f, condish, weather)
	f.close()

def markAsRead():
	while True :
		folder = voice.search('is:unread')
		if folder.totalSize <= 0:
			break
			util.print_(folder.totalSize)
		for message in folder.messages:
			util.print_(message)
			message.delete(1)

def deleteReadMessages():
	for message in voice.sms().messages:
	    if message.isRead:
	        message.delete()

def newLogIn():
	return 'New Log In'

def Shutdown():
	timeStampUUID = uuid.uuid1() #gwmi win32_bios | fl SerialNumber
	return 'Shutting down:\n' + str(timeStampUUID)

voice.login(NeedsEncryption, NeedsMoreEncryption)

while True:
	WeatherCommand = voice.search('Weather')
	LoggedCommand = voice.search('Logged')
	ShutDownCommand = voice.search('Shutdown')
	RebootCommand = voice.search('Reboot')
	if len(WeatherCommand) == 1:
		message = str(getTemp())
		voice.send_sms(sendTo, message)
		markAsRead()
		deleteReadMessages()
		print "Weather SMS Sent"
	elif len(LoggedCommand) == 1:
		message = str(newLogIn())
		voice.send_sms(sendTo, message)
		markAsRead()
		deleteReadMessages()
	elif len(ShutDownCommand) == 1:
		message = str(Shutdown())
		voice.send_sms(sendTo, message)
		markAsRead()
		deleteReadMessages()
		os.system('shutdown -s -t 0 /f')
	else:
		print 'Nuffin to see here'
		sleep(5)

computerLoggedInOrIsOn()
import urllib, json, sys, re
from datetime import datetime

api_key = '<API KEY>'

print('\033[1m'+"Precipitation Summary by City"+'\033[0m')
print
while(True):
	#get city
	city = raw_input("Which city would you like precipitation data for?: ")
	while not city:
		print
		print("No city was entered, please try again or type crtl+c to quit.")
		city = raw_input("Which city would you like precipitation data for?: ")
	
	#get number of days
	days = raw_input("How many days of precipitation data would you like? (max: 14): ")
	while not city or int(days) < 1 or int(days) > 14:
		print
		print("Invalid number of days were entered, please try again or type crtl+c to quit.")
		days = raw_input("How many days of summed precipitation data would you like? (max: 14): ")
	
	# clean up data
	city = city.strip()
	days = int(days)
	
	# get data from API
	url = "http://api.openweathermap.org/data/2.5/forecast/daily?q=" + city + "&mode=json&units=imperial&cnt=" + str(days) + "&appid="+api_key
	try:
		response = urllib.urlopen(url)
	except Exception as e:
		print
		print
		print("\033[1mERROR: Please be sure you have replaced <API KEY> with a valid API key from openweathermap.org and have entered a valid city name.\033[0m")
		sys.exit()
	

	# check if good response
	if response.code != 200:
		print
		print("ERROR: Please be sure you have replaced <API KEY> with a valid API key from openweathermap.org and have entered a valid city name.")
		sys.exit()

	# convert data to JSON
	data = json.loads(response.read())

	# run through data and sum up precipitation
	print
	print "\033[1mPrecipitation\033[0m (rain or snow):"
	print "Days: \033[1m" + str(days) + " days\033[0m"
	print "City: \033[1m" + city + "\033[0m"
	print "City Data: Country: \033[1m" + str(data['city']['country']) + "\033[0m Lat: \033[1m" + str(data['city']['coord']['lat']) + " \033[0mLon: \033[1m" + str(data['city']['coord']['lon']) + "\033[0m"
	day_list = data['list']
	total_precip = 0.0
	for day in day_list:
		if 'rain' in day:
			day_time = datetime.fromtimestamp(day['dt']).strftime("%a %b %d, %Y")
			total_precip += float(day['rain'])
			print("\033[1mRain\033[0m on \033[1m" + str(day_time) + "\033[0m")
		if 'snow' in day:
			day_time = datetime.fromtimestamp(day['dt']).strftime("%a %b %d, %Y")
			total_precip += float(day['snow'])
			print("\033[1mSnow\033[0m on \033[1m" + str(day_time) + "\033[0m")
	
	#print out analyzed precipitation data
	
	print "Total Precipitation over next " + str(days) + " days: \033[1m" + str(total_precip * 0.03937) + " inches \033[0mor\033[1m " + str(total_precip) + " mm\033[0m"
	
	print

	loop = raw_input("Type \033[1mquit\033[0m to end or Enter to continue: ")
	if loop == "quit" or loop == "q":
		sys.exit()
	print
	print
